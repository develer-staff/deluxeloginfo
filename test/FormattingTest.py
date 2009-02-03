import unittest;
import TestDLI

class TestFormatting(TestDLI.TestDLI):
    repository_name = 'base.svn'
    template_path = 'test/repository/base.svn.dump'

    # test "boring" hunks are skipped from diff
    def testBoringHunk(self):
        self.assertEqual(self.runDli(start_revision=12, end_revision=13), """
ChangeSet Index:

CS1 [#cs1] - Test boring hunks.

Test boring hunks.

M     13  trunk/keywords.txt

===================================================================
--- trunk/keywords.txt\t(revision 12)
+++ trunk/keywords.txt\t(revision 13)
@@ -14,7 +15,7 @@
 14
 15
 16
-17
+16bis
 18
 19
 20

Property changes on: keywords.txt
___________________________________________________________________
Added: svn:keywords
   + Id




""")

    # test long diffs are truncated
    def testLongDiff(self):
        self.assertEqual(self.runDli(start_revision=2, end_revision=3,
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
        self.assertEqual(self.runDli(start_revision=10, end_revision=11,
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
        self.assertEqual(self.runDli(start_revision=8, end_revision=9), """
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
        self.assertEqual(self.runDli(start_revision=9, end_revision=10,
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

if __name__ == '__main__':
    unittest.main()
