#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest;
import TestDLI

class TestStrangeFilenameSvn(TestDLI.TestDLI):
    repository_name = 'special.svn'
    template_path = 'test/repository/special.svn.dump'

    def testUTF(self):
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

if __name__ == '__main__':
    unittest.main()
