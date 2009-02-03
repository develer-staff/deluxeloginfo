import unittest;
import TestDLI

class TestTimeStamp(TestDLI.TestDLI):
    repository_name = 'timestamp.svn'
    template_path = 'test/repository/timestamp.svn.dump'
    start_timestamp = 4

    # one revision, using timestamp
    def testDiffOneRevBinaryChange(self):
        self.assertTimestamp(4)
        self.assertEqualDiff(self.runDli(), """
ChangeSet Index:

CS1 [#cs1] - Binary file modification.

Binary file modification.

M      5  [BIN] trunk/random.dat


""")
        self.assertTimestamp(5)

class TestMultiRevision(TestDLI.TestDLI):
    repository_name = 'timestamp.svn'
    template_path = 'test/repository/timestamp.svn.dump'
    start_timestamp = 0

    # multiple revisions, using timestamp
    def testMultipleRevBinaryChange(self):
        self.assertTimestamp(0)
        self.assertEqualDiff(self.runDli(), """
ChangeSet Index:

CS1 [#cs1] - Basic subversion structure.
CS2 [#cs2] - Added test file.
CS3 [#cs3] - Useless file modification.
CS4 [#cs4] - Binary file addition.
CS5 [#cs5] - Binary file modification.

Basic subversion structure.

A      1  branches
A      1  tags
A      1  trunk

===================================================================
--- /dev/null
+++ branches	(revision 1)

===================================================================
--- /dev/null
+++ tags	(revision 1)

===================================================================
--- /dev/null
+++ trunk	(revision 1)


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


Binary file addition.

A      4  [BIN] trunk/random.dat

Cannot display: file marked as a binary type.

Binary file modification.

M      5  [BIN] trunk/random.dat

Cannot display: file marked as a binary type.


""")
        self.assertTimestamp(5)

if __name__ == '__main__':
    unittest.main()
