#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest;
import dli_launcher

class TestLauncher(unittest.TestCase):
    def testReadPrjtab(self):
        self.assertEqual(dli_launcher.parse_prjtab('test/launcher/prjtab'),
                         [{'to': 'devtools@lists.develer.com',
                           'root': 'file:///svn',
                           'module': 'devtools'},
                          {'to': 'example@lists.develer.com',
                           'root': 'file:///svn',
                           'module': 'example',
                           }])

    def testReadDefaults(self):
        import ConfigParser

        parser = ConfigParser.SafeConfigParser()
        parser.read('test/launcher/defaults.ini')
        defaults = dli_launcher.read_options(parser, 'defaults')

        self.assertEqual(defaults,
                         {'index': 0,
                          'by_author': True,
                          'maildomain': 'develer.com',
                          'dli_path': '/usr/local/bin/deluxeloginfo',
                          'text': False,
                          'difflimit': 500,
                          'diff': True,
                          'branches': ['remote', 'master'],
                          'index_lines': 3})

    def testReadINI(self):
        self.assertEqual(dli_launcher.parse_ini_file('test/launcher/project.ini'),
                         [{'maildomain': 'develer.com',
                           'root': 'svn+ssh://test@example.com/svn',
                           'module': 'area-51',
                           'set_email': ['foo:moo@moo.com', 'roo:roo@moo.com'],
                           'bugurl': 'http://support.develer.com/bug.php?@BUG@',
                           'index_lines': 4,
                           'recipient': 'example@lists.develer.com',
                           },
                          {'maildomain': 'develer.com',
                           'root': 'svn+ssh://test@example.com/svn',
                           'module': 'mogul',
                           'bugurl': 'http://support.develer.com/bug.php?@BUG@',
                           'index_lines': 5,
                           'recipient': 'mogul@lists.develer.com',
                           }])

if __name__ == '__main__':
    unittest.main()
