import unittest
import subprocess
import re
import os
import string

# TODO (all file) use os.path

def repositoryUrl(name):
    return 'file://' + repositoryPath(name)

def repositoryPath(name):
    return os.path.abspath("test/repository/" + name)

class TestDLI(unittest.TestCase):
    # False if test modifies repository
    is_readonly = True
    # If set, (re)creates a .stamp file with the given value
    start_timestamp = None

    output_file = "test/tmp/output"

    def setupRepository(self, template, destination):
        subprocess.check_call(["svnadmin", "create", destination])
        subprocess.check_call("cat %s | svnadmin load %s" %
                                (template, destination), shell=True)

    def setupTimestamp(self, repository_url, value):
        stamp_path = "test/stamps/" + \
                       re.sub("[^a-zA-Z0-0]", "_", repository_url) + ".stamp"
        stamp = open(stamp_path, 'w')
        stamp.write(value)
        stamp.close()

    def runDli(self, start_revision=None, end_revision=None):
        if(os.access(self.output_file, os.F_OK)):
            os.remove(self.output_file)

        # FIXME more flexible argument handling
        more_args = []
        if (start_revision != None):
            more_args.append("--startrevision=" + str(start_revision))
        if (end_revision != None):
            more_args.append("--endrevision=" + str(end_revision))

        subprocess.check_call(["./deluxeloginfo", "--by-author",
                               "--rlog", "--diff", "--difflimit=500", 
                               "--index=0", "--index-lines=3",
                               "--root=" + repositoryUrl(self.repository_name),
                               "--encoding=utf-8", "--nohtml",
                               "--stampdir=test/stamps",
                               "--outfile=" + self.output_file] + more_args)

        # in some cases (for example empty revision range), no output
        # file is created
        if(not os.access(self.output_file, os.F_OK)):
            return None
        
        lines = open(self.output_file, "r").readlines()

        # remove header and signature
        del lines[0:lines.index("\n")]
        for i in xrange(len(lines) - 1, -1, -1):
            if lines[i] == "--\n":
                del lines[i:]
                break

        return string.join(lines, '')

    def setUp(self):
        # if readonly or not there must recreate from dump
        repo_path = repositoryPath(self.repository_name)
        if(not self.is_readonly or not os.access(repo_path, os.F_OK)):
            self.setupRepository(self.template_path, repo_path)

        if(self.start_timestamp != None):
            self.setupTimestamp(repositoryUrl(self.repository_name),
                                self.start_timestamp)
