#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest;
import TestDLI

class TestSvnBranch(TestDLI.TestDLI):
    repository_name = 'branch.svn'
    template_path = 'test/repository/branch.svn.dump'

    def testSvnTrunk(self):
        self.assertEqualDiff(self.runDli(start_revision=3, end_revision=4),
                             """
ChangeSet Index:

CS1 [#cs1] - Commit in trunk.

Commit in trunk.

M      4  trunk/test.txt

===================================================================
--- trunk/test.txt	(revision 3)
+++ trunk/test.txt	(revision 4)
@@ -1 +1 @@
-A test.
+In trunk.



""")

    def testSvnBranch(self):
        self.assertEqualDiff(self.runDli(start_revision=4, end_revision=5),
                             """
ChangeSet Index:

CS1 [#cs1] - Commit in branch.

 (on branch bough):
Commit in branch.

M      5  branches/bough/test.txt

===================================================================
--- branches/bough/test.txt	(revision 4)
+++ branches/bough/test.txt	(revision 5)
@@ -1 +1 @@
-A test.
+In branch.



""")

    def testSvnBranchAndTrunk(self):
        self.assertEqualDiff(self.runDli(start_revision=5, end_revision=6),
                             """
ChangeSet Index:

CS1 [#cs1] - Commit in both trunk and branch.

 (on branch bough, trunk):
Commit in both trunk and branch.

M      6  branches/bough/test.txt
M      6  trunk/test.txt

===================================================================
--- branches/bough/test.txt	(revision 5)
+++ branches/bough/test.txt	(revision 6)
@@ -1 +1 @@
-In branch.
+In branch (2)

===================================================================
--- trunk/test.txt	(revision 5)
+++ trunk/test.txt	(revision 6)
@@ -1 +1 @@
-In trunk.
+In trunk (2)



""")

if __name__ == '__main__':
    unittest.main()
