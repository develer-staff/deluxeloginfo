#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest;
import TestDLI

class TestStrangeFilenameSvn(TestDLI.TestDLI):
    repository_name = 'special.svn'
    template_path = 'test/repository/special.svn.dump'

    def testStrange(self):
        self.assertEqualDiff(self.runDli(start_revision=1, end_revision=2,
                                         show_text=True, show_html=False),
                             """
ChangeSet Index:

CS1 [#cs1] - Added a file with a funky name.

Added a file with a funky name.

A      2  foo-(1)#&$f.txt

===================================================================
--- /dev/null
+++ foo-(1)#&$f.txt	(revision 2)
+Strange name...



""")


class TestStrangeFilenameGit(TestDLI.TestDLI):
    repository_name = 'special.git'
    repository_type = 'git'
    repository_module = 'git' # to test that it is ignored
    template_path = 'test/repository/special.git.dump'

    def testStrange(self):
        self.assertEqualDiff(self.runDli(start_revision='760b618f', end_revision='4bb7a4bb',
                                         show_text=True, show_html=False),
                             """
ChangeSet Index:

CS1 [#cs1] - Added a file with a funky name.

Added a file with a funky name.

A 4bb7a4bbfcd702e86e822d9998a4e575a49db81e  foo-(1)#&$f.txt

======================================================================
--- /dev/null
+++ b/foo-(1)#&$f.txt
@@ -0,0 +1 @@
+Strange name...



""")


if __name__ == '__main__':
    unittest.main()
