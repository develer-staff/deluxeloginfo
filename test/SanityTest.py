import unittest;
import TestDLI
import os

class TestBasic(TestDLI.TestDLI):
    repository_name = 'base.svn'
    template_path = 'test/repository/base.svn.dump'

    def testDiffEmptyRevRange(self):
        self.assertEqual(self.runDli(start_revision=3, end_revision=3), None)

    def testDiffOneRevAddition(self):
        self.assertEqual(self.runDli(start_revision=1, end_revision=2), """
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
        self.assertEqual(self.runDli(start_revision=2, end_revision=3), """
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
        self.assertEqual(self.runDli(start_revision=3, end_revision=4), """
ChangeSet Index:

CS1 [#cs1] - Binary file addition.

Binary file addition.

A      4  [BIN] trunk/random.dat


""")

    def testDiffOneRevBinaryChange(self):
        self.assertEqual(self.runDli(start_revision=4, end_revision=5), """
ChangeSet Index:

CS1 [#cs1] - Binary file modification.

Binary file modification.

M      5  [BIN] trunk/random.dat


""")

class TestTimeStamp(TestDLI.TestDLI):
    repository_name = 'base.svn'
    template_path = 'test/repository/base.svn.dump'
    start_timestamp = 4

    def testDiffOneRevBinaryChange(self):
        self.assertTimestamp(4)
        self.assertEqual(self.runDli(), """
ChangeSet Index:

CS1 [#cs1] - Binary file modification.

Binary file modification.

M      5  [BIN] trunk/random.dat


""")
        self.assertTimestamp(5)

if __name__ == '__main__':
    unittest.main()
