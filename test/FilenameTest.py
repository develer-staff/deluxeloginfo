#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest;
import TestDLI

class TestStrangeFilenameSvn(TestDLI.TestDLI):
    repository_name = 'special.svn'
    template_path = 'test/repository/special.svn.dump'

    def testStrange(self):
        self.assertEqualDiff(self.runDli(start_revision=1, end_revision=3,
                                         show_text=True, show_html=False),
                             """
ChangeSet Index:

CS1 [#cs1] - Added a file with a funky name.
CS2 [#cs2] - Sorry, forgot some.

Added a file with a funky name.

A      2  foo-(1)#&$f.txt

===================================================================
--- /dev/null
+++ foo-(1)#&$f.txt	(revision 2)
+Strange name...


Sorry, forgot some.

D      2  foo-(1)#&$f.txt
M      3  foo: space,	tab<|.txt


""")


class TestStrangeFilenameGit(TestDLI.TestDLI):
    repository_name = 'special.git'
    repository_type = 'git'
    repository_module = 'git' # to test that it is ignored
    template_path = 'test/repository/special.git.dump'

    def testStrange(self):
        self.assertEqualDiff(self.runDli(start_revision='760b618f', end_revision='d480cff7',
                                         show_text=True, show_html=False),
                             """
ChangeSet Index:

CS1 [#cs1] - Added a file with a funky name.
CS2 [#cs2] - Sorry, forgot some.

Added a file with a funky name.

A 4bb7a4bbfcd702e86e822d9998a4e575a49db81e  foo-(1)#&$f.txt

======================================================================
--- /dev/null
+++ b/foo-(1)#&$f.txt
@@ -0,0 +1 @@
+Strange name...


Sorry, forgot some.

M d480cff78fa1af01b0a62875e2a2181607bd9f88  "foo: space,\\ttab<|.txt"
D 4bb7a4bbfcd702e86e822d9998a4e575a49db81e  foo-(1)#&$f.txt


""")


if __name__ == '__main__':
    unittest.main()
