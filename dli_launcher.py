#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Copyright 2009 Develer S.r.l. (http://www.develer.com/)
# All rights reserved.
#
# $Id$
#
# Author: Mattia Barbon <mattia@develer.com>
#

import ConfigParser
import optparse
import sys
import subprocess
import os.path
import os

INT_OPTIONS = set(["difflimit", "index", "index_lines"])
BOOL_OPTIONS = set(["by_author", "diff", "html", "text"])

def abort(message):
    print >>sys.stderr, message

    sys.exit(1)

def parse_options():
    """
    Parse command line options, return a (dictionary, list) pair
    with the parsed options in the dictionary and the arguments in the
    list.
    """
    usage = "Usage: %prog [options] [file|directory]"
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("--defaults", metavar="FILE",
                      help="read default options from FILE")
    parser.add_option("--prjtab", action='store_true',
                      help="assume files are in prjtab format")
    parser.add_option("--dli-path", metavar="FILE",
                      help="path to deluxeloginfo executable")

    parser.add_option("-v", "--verbose", action="store_true",
                      help="print deluxeloginfo invocations")
    parser.add_option("--dry-run", action="store_true",
                      help="do not execute deluxeloginfo")

    repo = optparse.OptionGroup(parser, "Deluxeloginfo repository options")
    repo.add_option("--stampdir", metavar="DIR",
                      help="where to store timestamps for cvs rlog and svn log")
    repo.add_option("--branches", metavar="[local|remote|all|<branch-name>]",
                      action="append",
                      help="branches to track (Git only); \
can be specified multiple times")
    parser.add_option_group(repo)

    output = optparse.OptionGroup(parser, "Deluxeloginfo output redirection")
    output.add_option("--sender", metavar="ADDR",
                      help="sender e-mail address for log messages")
    output.add_option("--maildomain", metavar="DOMAIN",
                      help="mail domain for committers (used for From:)")
    output.add_option("--to", metavar="ADDR",
                      help="comma-separated list of mail recipients");
    parser.add_option_group(output)

    format = optparse.OptionGroup(parser, "Deluxeloginfo output format")
    format.add_option("--by-author", action="store_true",
                      help="send one mail for each committer")
    format.add_option("--diff", action="store_true",
                      help="show diff for commits")
    format.add_option("--difflimit", metavar="N", type="int",
                      help="show up to N lines of diff output")
    format.add_option("--index", metavar="N", type="int",
                      help="output a summary of ChangeSets.  If N is specified \
the index is printed only when it contains at least N ChangeSets. \
Set to 0 to always print the index")
    format.add_option("--index-lines", metavar="N", type="int",
                      help="number of log lines in an index entry")
    format.add_option("--notext", action="store_false", dest="text",
                      help="disable text output")
    format.add_option("--nohtml", action="store_false", dest="html",
                      help="disable HTML output")
    parser.add_option_group(format)

    weblink = optparse.OptionGroup(parser, "Deluxeloginfo web link generation")
    weblink.add_option("--weburl", metavar="URL",
                       help="set URL for web revision history viewer")
    weblink.add_option("--bugurl", metavar="URL",
                       help="set URL for bug database")
    parser.add_option_group(weblink)

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    return (options.__dict__, args)

def parse_prjtab(prjtab):
    """
    Parse a prjtab file and return a list containing one dictionary
    witk keys (to, root, module) for each non-empty line in the file.
    """
    commands = []

    for line in open(prjtab):
        # skip empty/commented lines
        line = line.strip()
        if line.startswith("#"):
            continue
        if not line:
            continue

        (module, root, email) = line.split(None, 3)

        if not module or not root or not email:
            abort("Illegal prjtab format: '%s'" % line)

        commands.append({"to": email, "root": root,"module": module})

    return commands

def format_arguments(command):
    """
    Take a dictionary containing command-line options and transform it
    in a deluxeloginfo invocation.  All key/value pairs are formatted
    as --key=value, except: by_author, diff, html, text are converted
    to the corresponding boolean options, dli_path is used as the
    deluxeloginfo path.
    """
    args = []

    dli_path = None
    for (key, value) in command.items():
        if value == None:
            continue

        if key == 'branches':
            args.extend(["--branch=%s" % i for i in value])
        elif key == 'by_author':
            if value:
                args.append("--by-author")
        elif key == 'diff':
            if value:
                args.append("--diff")
        # negated options are a pain
        elif key == 'html':
            if value != None and not value:
                args.append("--nohtml")
        elif key == 'text':
            if value != None and not value:
                args.append("--notext")
        elif key == 'dli_path':
            dli_path = value
        else:
            args.append("--%s=%s" % (key.replace('_', '-'), value))

    if not dli_path:
        abort("dli_path must be specified to run deluxeloginfo")

    return [dli_path] + args

def read_options(config, section, defaults=dict()):
    """
    Return a dictionary with all the options in the given section of
    the ConfigParser object.  Read options listed in INT_OPTIONS and
    BOOL_OPTIONS as int/boolean, the rest as strings.
    """
    options = dict(defaults)

    for opt in config.options(section):
        if opt == 'branches':
            options[opt] = config.get(section, opt).split(',')
        elif opt in BOOL_OPTIONS:
            options[opt] = config.getboolean(section, opt)
        elif opt in INT_OPTIONS:
            options[opt] = config.getint(section, opt)
        else:
            options[opt] = config.get(section, opt)

    return options

def parse_ini_file(file):
    """
    Parse an ini file and return a list of all the options in all the sections.
    """
    parser = ConfigParser.SafeConfigParser()
    parser.read(file)

    if parser.has_section('defaults'):
        defaults = read_options(parser, 'defaults')
    else:
        defaults = dict()

    options = []
    for section in parser.sections():
        if section == 'defaults':
            continue

        options.append(read_options(parser, section, defaults))

    return options

def execute_dli(command, verbose=False, dry_run=False):
    """
    Take a deluxeloginfo invocation and print and/or execute it
    depending on verbose/dry_run settings
    """
    args = format_arguments(command)
    if verbose or dry_run:
        print " ".join(args)
    if not dry_run:
        subprocess.check_call(args)

def main():
    (options, args) = parse_options()
    defaults_file = options.pop('defaults')
    verbose = options.pop('verbose')
    dry_run = options.pop('dry_run')
    is_prjtab = options.pop('prjtab')

    # clean options to be passed to deluxeloginfo
    for (key, value) in options.items():
        if value == None:
            del options[key]

    # read defaults file
    if defaults_file:
        parser = ConfigParser.SafeConfigParser()
        parser.read(defaults_file)
        defaults = read_options(parser, 'defaults')
    else:
        defaults = dict()

    # read commands from prjtab/config file/config directory
    cmd_list = []
    for path in args:
        if os.path.isfile(path):
            if is_prjtab:
                cmd_list.extend(parse_prjtab(path))
            else:
                cmd_list.extend(parse_ini_file(path))
        elif os.path.isdir(path):
            for file in map(lambda x: os.path.join(path, x), os.listdir(path)):
                if os.path.isfile(file):
                    cmd_list.extend(parse_ini_file(file))
        else:
            abort("Path '%s' is neither file nor directory" % path)

    # merge defaults and command-line options and call deluxeloginfo
    for cmd in cmd_list:
        command = dict(defaults)
        command.update(cmd)
        command.update(options)

        execute_dli(command, dry_run=dry_run, verbose=verbose)

if __name__ == '__main__':
    main()
