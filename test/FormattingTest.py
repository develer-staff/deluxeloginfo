#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest;
import TestDLI

class TestFormatting(TestDLI.TestDLI):
    repository_name = 'base.svn'
    template_path = 'test/repository/base.svn.dump'

    # test "boring" hunks are skipped from diff
    def testBoringHunk(self):
        self.assertEqualDiff(self.runDli(start_revision=14, end_revision=15),
                             """
ChangeSet Index:

CS1 [#cs1] - Test.

Test.

M     15  trunk/keywords.txt

===================================================================
--- trunk/keywords.txt\t(revision 14)
+++ trunk/keywords.txt\t(revision 15)
@@ -15,7 +15,7 @@
 14
 15
 16
-16bis
+17
 18
 19
 20



""")

    # test long diffs are truncated
    def testLongDiff(self):
        self.assertEqualDiff(self.runDli(start_revision=2, end_revision=3,
                                         diff_limit=6), """
ChangeSet Index:

CS1 [#cs1] - Useless file modification.

Useless file modification.

M      3  trunk/README.txt

===================================================================
--- trunk/README.txt	(revision 2)
+++ trunk/README.txt	(revision 3)
@@ -1,7 +1,4 @@
-Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod
+  Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod
*** SIZE LIMIT EXCEEDED - DIFF TRUNCATED ***


""")

    # test long diff lines weight more than short ones
    # when computing diff size
    def testLongDiffLines(self):
        self.assertEqualDiff(self.runDli(start_revision=10, end_revision=11,
                                         diff_limit=10), """
ChangeSet Index:

CS1 [#cs1] - File with long lines.

File with long lines.

A     11  trunk/file_with_long_lines.txt

===================================================================
--- /dev/null
+++ trunk/file_with_long_lines.txt\t(revision 11)
+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
*** SIZE LIMIT EXCEEDED - DIFF TRUNCATED ***


""")

    def testEmptyLogMessage(self):
        self.assertEqualDiff(self.runDli(start_revision=8, end_revision=9), """
ChangeSet Index:

CS1 [#cs1] - *** Empty log message! ***

*** Empty log message! ***
A      9  trunk/empty_log_message.txt

===================================================================
--- /dev/null
+++ trunk/empty_log_message.txt	(revision 9)



""")

    # long log messare is truncated in index
    def testLongLogMessage(self):
        self.assertEqualDiff(self.runDli(start_revision=9, end_revision=10,
                                         index_lines=2), """
ChangeSet Index:

CS1 [#cs1] - Log message with
multiple lines[...]

Log message with
multiple lines
to test truncation
when displayed
inside index.

D      9  trunk/empty_log_message.txt


""")

    # test with latin1 characters
    def testNonAsciiChars(self):
        self.assertEqualDiff(self.runDli(start_revision=13, end_revision=14),
                             u"""
ChangeSet Index:

CS1 [#cs1] - Test lettere accentate: àèìòù.

Test lettere accentate: àèìòù.

M     14  trunk/README.txt

===================================================================
--- trunk/README.txt	(revision 13)
+++ trunk/README.txt	(revision 14)
@@ -2,3 +2,5 @@
 tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim
 veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex
 ea commodi consequat.
+
+  Test lettere accentate: àèìòù.



""")

class TestFormattingGit(TestDLI.TestDLI):
    repository_name = 'latin1.git'
    repository_type = 'git'
    template_path = 'test/repository/latin1.git.dump'

    # test with latin1 characters
    def testNonAsciiChars(self):
        self.assertEqualDiff(self.runDli(start_revision='144c3ba9',
                                         end_revision='30fbdf4'),
                             u"""
ChangeSet Index:

CS1 [#cs1] - Another test latin1 àèìòù.

Another test latin1 àèìòù.

M 30fbdf4975c0c49d3591e5506d6c33afa3b4ca8e  test_latin1.txt

======================================================================
--- a/test_latin1.txt
+++ b/test_latin1.txt
@@ -1 +1 @@
-Test latin1 àèìòù.
+Another test latin1 àèìòù.



""")

    # test changes on multiple files
    def testNonAsciiChars(self):
        self.assertEqualDiff(self.runDli(start_revision='aaa1319c',
                                         end_revision='6ac11816'),
                             """
ChangeSet Index:

CS1 [#cs1] - Change two files.

Change two files.

A 6ac1181609dc7ca112a942fce6e7cb6b45cd45a7  test2.txt
A 6ac1181609dc7ca112a942fce6e7cb6b45cd45a7  test_latin1.txt

======================================================================
--- /dev/null
+++ b/test2.txt
@@ -0,0 +1 @@
+Change two files.

======================================================================
--- a/test_latin1.txt
+++ b/test_latin1.txt
@@ -1 +1 @@
-Test bugzillate.
+Test two files.



""")

if __name__ == '__main__':
    unittest.main()
