#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
import subprocess
import re
import os
import string
import difflib
import codecs

# TODO (all file) use os.path

def repositoryUrl(type, name):
    if type == 'svn':
        return 'file://' + repositoryPath(name)
    else:
        return repositoryPath(name)

def repositoryPath(name):
    return os.path.abspath("test/repository/" + name)

def timestampPath(repository_url):
        return "test/stamps/" + \
            re.sub("[^a-zA-Z0-9]", "_", repository_url) + ".stamp"

class TestDLI(unittest.TestCase):
    # 'svn' or 'git'
    repository_type = 'svn'
    # False if test modifies repository
    is_readonly = True
    # If set, (re)creates a .stamp file with the given value
    start_timestamp = None

    output_file = "test/tmp/output"

    def assertEqualDiff(self, first, second, msg=None):
        if not first == second:
            diff = difflib.unified_diff(string.split(first, "\n"),
                                        string.split(second, "\n"),
                                        fromfile="got", tofile="expected",
                                        lineterm="")
            raise self.failureException, \
                (msg or "\n" + string.join(diff, "\n"))

    def setupSvnRepository(self, template, destination):
        subprocess.check_call(["svnadmin", "create", destination])
        subprocess.check_call("cat %s | svnadmin load %s" %
                                (template, destination), shell=True)

    def setupGitRepository(self, template, destination):
        subprocess.check_call(["git", "--git-dir=%s" % destination, "init"])
        subprocess.check_call("cat %s | git --git-dir=%s fast-import" %
                                (template, destination), shell=True)

    def setupTimestamp(self, repository_url, value):
        stamp = open(timestampPath(repository_url), 'w')
        stamp.write(str(value))
        stamp.close()

    def assertTimestamp(self, value):
        stamp = open(timestampPath(repositoryUrl(self.repository_type,
                                                 self.repository_name)), 'r')
        self.assertEqual(stamp.readline(), str(value))

    def runDli(self, start_revision=None, end_revision=None, show_diff=True,
               diff_limit=500, index_entries=0, index_lines=3,
               show_text=True, show_html=False):
        if os.access(self.output_file, os.F_OK):
            os.remove(self.output_file)

        more_args = []
        if start_revision != None:
            more_args.append("--startrevision=" + str(start_revision))
        if end_revision != None:
            more_args.append("--endrevision=" + str(end_revision))
        if show_diff: more_args.append("--diff")
        if diff_limit != None:
            more_args.append("--difflimit=" + str(diff_limit))
        if index_entries != None:
            more_args.append("--index=" + str(index_entries))
        if index_lines != None:
            more_args.append("--index-lines=" + str(index_lines))
        if not show_text: more_args.append("--notext")
        if not show_html: more_args.append("--nohtml")

        subprocess.check_call(["./deluxeloginfo", "--by-author", "--rlog",
                               "--root=" + repositoryUrl(self.repository_type,
                                                         self.repository_name),
                               "--encoding=utf-8", "--stampdir=test/stamps",
                               "--outfile=" + self.output_file] + more_args)

        # in some cases (for example empty revision range), no output
        # file is created
        if not os.access(self.output_file, os.F_OK):
            return None
        
        binary_handle = open(self.output_file, "r")
        reader = codecs.getreader("utf-8")(binary_handle)
        lines = reader.readlines()

        # remove header and signature
        if show_text:
            del lines[0:lines.index("\n")]
            for i in xrange(len(lines) - 1, -1, -1):
                if lines[i] == "--\n":
                    del lines[i:]
                    break
        elif show_html:
            del lines[0:lines.index("</head>\n") + 1]
            for i in xrange(len(lines) - 1, -1, -1):
                if lines[i] == "<p>--<br />\n":
                    del lines[i:]
                    break

        return string.join(lines, '')

    def setUp(self):
        # if readonly or not there must recreate from dump
        repo_path = repositoryPath(self.repository_name)
        if not self.is_readonly or not os.access(repo_path, os.F_OK):
            if self.repository_type == 'svn':
                self.setupSvnRepository(self.template_path, repo_path)
            else:
                self.setupGitRepository(self.template_path, repo_path)
        if self.start_timestamp != None:
            self.setupTimestamp(repositoryUrl(self.repository_type,
                                              self.repository_name),
                                self.start_timestamp)
