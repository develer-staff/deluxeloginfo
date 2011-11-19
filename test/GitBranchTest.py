#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest;
import TestDLI

class TestGitBranchTracking(TestDLI.TestDLI):
    repository_name = 'base.git'
    repository_type = 'git'
    template_path = 'test/repository/base.git.dump'

    def testDiffChangesInBranch(self):
        self.assertEqualDiff(self.runDli(start_revision='bdb46855^',
                                         end_revision='9209bd90'), """
ChangeSet Index:

CS1 [#cs1] - Commit in first_branch.
CS2 [#cs2] - Another commit in first_branch.
CS3 [#cs3] - Third commit in first_branch.

Commit in first_branch.

M bdb46855d8872f65b2e3b2607934313b948b5688  README.txt
D f9b4c81c9c0d64e956d9dcd011e750544938a518  add_file.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,3 +1,5 @@
+Commit in first_branch.
+
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.
 


Another commit in first_branch.

M ba96d7770b9a160f4fb38aa10a9fc6aecb3ef614  README.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,4 +1,4 @@
-Commit in first_branch.
+Another commit in first_branch.
 
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.


Third commit in first_branch.

M 9209bd9009b1cbbc09c23e446fc714ef39964baf  README.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,4 +1,4 @@
-Another commit in first_branch.
+Commit in first_branch but not in second_branch.
 
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.



""")

class TestGitMergeLog(TestDLI.TestDLI):
    repository_name = 'base.git'
    repository_type = 'git'
    template_path = 'test/repository/base.git.dump'

    def testBranchTracking(self):
        self.setTimestamp("""
f9b4c81c9c0d64e956d9dcd011e750544938a518 first_branch
f9b4c81c9c0d64e956d9dcd011e750544938a518 master
ba96d7770b9a160f4fb38aa10a9fc6aecb3ef614 second_branch
""")
        self.assertEqualDiff(self.runDli(), """
ChangeSet Index:

CS1 [#cs1] - Commit in first_branch.
CS2 [#cs2] - Another commit in first_branch.
CS3 [#cs3] - Commit in second branch.
CS4 [#cs4] - Third commit in first_branch.
CS5 [#cs5] - Commit in master.

 (on branch first_branch):
Commit in first_branch.

M bdb46855d8872f65b2e3b2607934313b948b5688  README.txt
D f9b4c81c9c0d64e956d9dcd011e750544938a518  add_file.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,3 +1,5 @@
+Commit in first_branch.
+
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.
 


 (on branch first_branch):
Another commit in first_branch.

M ba96d7770b9a160f4fb38aa10a9fc6aecb3ef614  README.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,4 +1,4 @@
-Commit in first_branch.
+Another commit in first_branch.
 
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.


 (on branch second_branch):
Commit in second branch.

M 00f60cd27c6f572fae306a01444ad9b1d85b1c6d  README.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,4 +1,4 @@
-Another commit in first_branch.
+Commit in second_branch.
 
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.


 (on branch first_branch):
Third commit in first_branch.

M 9209bd9009b1cbbc09c23e446fc714ef39964baf  README.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,4 +1,4 @@
-Another commit in first_branch.
+Commit in first_branch but not in second_branch.
 
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.


 (on branch master):
Commit in master.

M 218593eb78da09a6c4c15f63d1fbafdf64c27c4f  README.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,3 +1,5 @@
+Commit in master.
+
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.
 



""")
        self.assertTimestamp(
"""9209bd9009b1cbbc09c23e446fc714ef39964baf first_branch
218593eb78da09a6c4c15f63d1fbafdf64c27c4f master
00f60cd27c6f572fae306a01444ad9b1d85b1c6d second_branch
""")

    # everything in second branch has already been logged (including
    # first two commits of first_branch) so only the last commit of
    # first branch remains
    def testNewBranchTracking(self):
        self.setTimestamp("""
218593eb78da09a6c4c15f63d1fbafdf64c27c4f master
00f60cd27c6f572fae306a01444ad9b1d85b1c6d second_branch
""")
        self.assertEqualDiff(self.runDli(), """
ChangeSet Index:

CS1 [#cs1] - Third commit in first_branch.

 (on branch first_branch):
Third commit in first_branch.

M 9209bd9009b1cbbc09c23e446fc714ef39964baf  README.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,4 +1,4 @@
-Another commit in first_branch.
+Commit in first_branch but not in second_branch.
 
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.



""")
        self.assertTimestamp(
"""9209bd9009b1cbbc09c23e446fc714ef39964baf first_branch
218593eb78da09a6c4c15f63d1fbafdf64c27c4f master
00f60cd27c6f572fae306a01444ad9b1d85b1c6d second_branch
""")

    # when two branches are started, common commits are reported only
    # once and only in one branch
    def testNewBranchesCommonPart(self):
        self.setTimestamp("""
218593eb78da09a6c4c15f63d1fbafdf64c27c4f master
""")
        self.assertEqualDiff(self.runDli(), """
ChangeSet Index:

CS1 [#cs1] - Commit in first_branch.
CS2 [#cs2] - Another commit in first_branch.
CS3 [#cs3] - Commit in second branch.
CS4 [#cs4] - Third commit in first_branch.

 (on branch first_branch):
Commit in first_branch.

M bdb46855d8872f65b2e3b2607934313b948b5688  README.txt
D f9b4c81c9c0d64e956d9dcd011e750544938a518  add_file.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,3 +1,5 @@
+Commit in first_branch.
+
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.
 


 (on branch first_branch):
Another commit in first_branch.

M ba96d7770b9a160f4fb38aa10a9fc6aecb3ef614  README.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,4 +1,4 @@
-Commit in first_branch.
+Another commit in first_branch.
 
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.


 (on branch second_branch):
Commit in second branch.

M 00f60cd27c6f572fae306a01444ad9b1d85b1c6d  README.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,4 +1,4 @@
-Another commit in first_branch.
+Commit in second_branch.
 
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.


 (on branch first_branch):
Third commit in first_branch.

M 9209bd9009b1cbbc09c23e446fc714ef39964baf  README.txt

======================================================================
--- a/README.txt
+++ b/README.txt
@@ -1,4 +1,4 @@
-Another commit in first_branch.
+Commit in first_branch but not in second_branch.
 
 Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
 eiusmod tempor incididunt ut labore et dolore magna aliqua.



""")
        self.assertTimestamp(
"""9209bd9009b1cbbc09c23e446fc714ef39964baf first_branch
218593eb78da09a6c4c15f63d1fbafdf64c27c4f master
00f60cd27c6f572fae306a01444ad9b1d85b1c6d second_branch
""")

if __name__ == '__main__':
    unittest.main()
