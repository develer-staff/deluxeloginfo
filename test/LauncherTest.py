#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest;
import dli_launcher

class TestLauncherParser(unittest.TestCase):
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

class TestLauncherExecute(unittest.TestCase):
    def testCommandFailureNoOutput(self):
        success, diag = dli_launcher.execute_dli(
            {'dli_path': '/ffdjd'})

        self.assertFalse(success)
        self.assertTrue(diag.startswith('/ffdjd\n'))

        success, diag = dli_launcher.execute_dli(
            {'dli_path': 'false'})

        self.assertFalse(success)
        self.assertEquals(diag, 'false\n')

        success, diag = dli_launcher.execute_dli(
            {'dli_path': 'false'}, verbose=True)

        self.assertFalse(success)
        self.assertEquals(diag, 'false\n')

    def testCommandFailureWithOutput(self):
        success, diag = dli_launcher.execute_dli(
            {'dli_path': 'test/launcher/noisy_failure'})

        self.assertFalse(success)
        self.assertEquals(diag,
                          'test/launcher/noisy_failure\n'
                          'Fail noisily\n')

        success, diag = dli_launcher.execute_dli(
            {'dli_path': 'test/launcher/noisy_failure'}, verbose=True)

        self.assertFalse(success)
        self.assertEquals(diag,
                          'test/launcher/noisy_failure\n'
                          'Fail noisily\n')

    def testCommandSuccessNoOutput(self):
        success, diag = dli_launcher.execute_dli(
            {'dli_path': 'true'})

        self.assertTrue(success)
        self.assertEquals(diag, '')

        success, diag = dli_launcher.execute_dli(
            {'dli_path': 'true'}, verbose=True)

        self.assertTrue(success)
        self.assertEquals(diag, 'true\n')

    def testCommandSuccessWithOutput(self):
        success, diag = dli_launcher.execute_dli(
            {'dli_path': 'test/launcher/noisy_success'})

        self.assertTrue(success)
        self.assertEquals(diag,
                          'test/launcher/noisy_success\n'
                          'Succeed noisily\n')

        success, diag = dli_launcher.execute_dli(
            {'dli_path': 'test/launcher/noisy_success'}, verbose=True)

        self.assertTrue(success)
        self.assertEquals(diag,
                          'test/launcher/noisy_success\n'
                          'Succeed noisily\n')

    def testDryRun(self):
        success, diag = dli_launcher.execute_dli(
            {'dli_path': 'true'}, dry_run=True)

        self.assertTrue(success)
        self.assertEquals(diag, 'true\n')

        success, diag = dli_launcher.execute_dli(
            {'dli_path': 'false'}, dry_run=True)

        self.assertTrue(success)
        self.assertEquals(diag, 'false\n')


if __name__ == '__main__':
    unittest.main()
