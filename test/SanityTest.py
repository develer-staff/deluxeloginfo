#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest;
import TestDLI

class TestBasic(TestDLI.TestDLI):
    repository_name = 'base.svn'
    template_path = 'test/repository/base.svn.dump'

    def testDiffEmptyRevRange(self):
        self.assertEqualDiff(self.runDli(start_revision=3, end_revision=3),
                             None)

    def testDiffOneRevAddition(self):
        self.assertEqualDiff(self.runDli(start_revision=1, end_revision=2), """
ChangeSet Index:

CS1 [#cs1] - Added test file.

Added test file.

A      2  trunk/README.txt

===================================================================
--- /dev/null
+++ trunk/README.txt	(revision 2)
+Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod
+tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim
+veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex
+ea commodi consequat. Quis aute iure reprehenderit in voluptate velit
+esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat
+cupiditat non proident, sunt in culpa qui officia deserunt mollit anim
+id est laborum.



""")

    def testDiffOneRevChange(self):
        self.assertEqualDiff(self.runDli(start_revision=2, end_revision=3), """
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
 tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim
 veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex
-ea commodi consequat. Quis aute iure reprehenderit in voluptate velit
-esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat
-cupiditat non proident, sunt in culpa qui officia deserunt mollit anim
-id est laborum.
+ea commodi consequat.



""")

    def testDiffOneRevBinaryAddition(self):
        self.assertEqualDiff(self.runDli(start_revision=3, end_revision=4), """
ChangeSet Index:

CS1 [#cs1] - Binary file addition.

Binary file addition.

A      4  [BIN] trunk/random.dat


""")

    def testDiffOneRevBinaryChange(self):
        self.assertEqualDiff(self.runDli(start_revision=4, end_revision=5), """
ChangeSet Index:

CS1 [#cs1] - Binary file modification.

Binary file modification.

M      5  [BIN] trunk/random.dat


""")

    def testDiffOneRevCopy(self):
        self.assertEqualDiff(self.runDli(start_revision=5, end_revision=6), """
ChangeSet Index:

CS1 [#cs1] - Test copy.

Test copy.

M      6  trunk/README.copy


""")

    def testDiffOneRevRename(self):
        self.assertEqualDiff(self.runDli(start_revision=6, end_revision=7), """
ChangeSet Index:

CS1 [#cs1] - Test rename.

Test rename.

D      6  trunk/README.copy
M      7  trunk/README.move


""")

    def testDiffOneRevDelete(self):
        self.assertEqualDiff(self.runDli(start_revision=7, end_revision=8), """
ChangeSet Index:

CS1 [#cs1] - Test delete.

Test delete.

D      7  trunk/README.move


""")

class TestBasicGit(TestDLI.TestDLI):
    repository_name = 'base.git'
    repository_type = 'git'
    template_path = 'test/repository/base.git.dump'

    def testDiffOneRevChange(self):
        self.assertEqualDiff(self.runDli(start_revision="e1b4ebaa1",
                                         end_revision="bffc9b15"), """
ChangeSet Index:

CS1 [#cs1] - Another formatting change.

Another formatting change.

M bffc9b150529f11fe676839eab6ae763153d963e  README.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,7 +1,7 @@
-  Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
+Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.
 
-  Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
+Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
 nisi ut aliquip ex ea commodo consequat.
 
   Duis aute irure dolor in reprehenderit in voluptate velit esse



""")

    def testDiffOneRevAddition(self):
        self.assertEqualDiff(self.runDli(start_revision="f72d8aa5541",
                                         end_revision="d476f89be83"), """
ChangeSet Index:

CS1 [#cs1] - File addition.

File addition.

A d476f89be8300b539a346d2dc311f385ff35a1e9  add_file.txt

======================================================================
--- /dev/null
+++ b/add_file.txt
@@ -0,0 +1 @@
+Added file.



""")

    def testDiffOneRevCopy(self):
        self.assertEqualDiff(self.runDli(start_revision="d476f89be83",
                                         end_revision="5f56b1035d09"), """
ChangeSet Index:

CS1 [#cs1] - Copied file.

Copied file.

M 5f56b1035d098c465ac6fcac39a9cb3fe2a75254  copy_file.txt


""")

    def testDiffOneRevRename(self):
        self.assertEqualDiff(self.runDli(start_revision="5f56b1035d09",
                                         end_revision="8df793771ac4"), """
ChangeSet Index:

CS1 [#cs1] - Rename file.

Rename file.

D 5f56b1035d098c465ac6fcac39a9cb3fe2a75254  copy_file.txt
M 8df793771ac452c5be95630e4a5e56030f7156d4  rename_file.txt


""")

    def testDiffOneRevDelete(self):
        self.assertEqualDiff(self.runDli(start_revision="8df793771ac4",
                                         end_revision="c94ffe16f76660"), """
ChangeSet Index:

CS1 [#cs1] - Removed file.

Removed file.

D 8df793771ac452c5be95630e4a5e56030f7156d4  rename_file.txt


""")

    def testDiffOneRevBinaryAddition(self):
        self.assertEqualDiff(self.runDli(start_revision='c94ffe16f7666',
                                         end_revision='af9ddcc9efa8aa8'), """
ChangeSet Index:

CS1 [#cs1] - Binary file add.

Binary file add.

A af9ddcc9efa8aa8273ccd21177a5b99ce2d24389  [BIN] random.dat


""")

    def testDiffOneRevBinaryChange(self):
        self.assertEqualDiff(self.runDli(start_revision='ea57c1c06ad41',
                                         end_revision='f9b4c81c9c0d'), """
ChangeSet Index:

CS1 [#cs1] - Binary file change.

Binary file change.

M f9b4c81c9c0d64e956d9dcd011e750544938a518  [BIN] random.dat


""")


if __name__ == '__main__':
    unittest.main()
