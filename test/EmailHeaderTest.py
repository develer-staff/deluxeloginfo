#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest;
import TestDLI

class TestEmailHeaderGit(TestDLI.TestDLI):
    repository_name = 'base.git'
    repository_type = 'git'
    template_path = 'test/repository/base.git.dump'

    def testBasicHeader(self):
        self.assertEqualDiff(self.runDli(start_revision='f9b4c81c9',
                                         end_revision='218593eb7',
                                         show_text=False, show_header=True),
                             """
From: Mattia Barbon <mattia@monolith.(none)>
Subject: changes by Mattia Barbon <mattia@monolith.(none)> (DATE)
""")

    def testModuleDescription(self):
        self.assertEqualDiff(self.runDli(start_revision='f9b4c81c9',
                                         end_revision='218593eb7',
                                         module_description='Test repo',
                                         show_text=False, show_header=True),
                             """
From: Mattia Barbon <mattia@monolith.(none)>
Subject: changes by Mattia Barbon <mattia@monolith.(none)> for Test repo (DATE)
""")


if __name__ == '__main__':
    unittest.main()
