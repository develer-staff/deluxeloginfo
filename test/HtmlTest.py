#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest;
import TestDLI
import re

class TestHtml(TestDLI.TestDLI):
    boring_attributes = ["text", "bgcolor", "colspan", "border",
                         "cellspacing", "cellpadding", "width", "color"]
    remove_attributes = "(?:%s)=(['\"])[^'\"]+(['\"]) ?" % \
        "|".join(boring_attributes)

    def assertHtmlEqual(self, first, second, msg=None):
        # strip 'uninteresting' attributes
        cleaned = re.sub(self.remove_attributes, "", first)
        cleaned = re.sub("<(\w+) >", "<\\1>", cleaned)

        self.assertEqualDiff(cleaned, second, msg)

class TestSvnHtml(TestHtml):
    repository_name = 'base.svn'
    template_path = 'test/repository/base.svn.dump'

    # one revision, using timestamp
    def testHtml(self):
        self.assertHtmlEqual(self.runDli(start_revision=1, end_revision=4,
                                         show_text=False, show_html=True),
                             """<body>
<h3>ChangeSet Index:</h3>
<ul>
<li><a href='#cs1'>CS1</a> - Added test file.</li>
<li><a href='#cs2'>CS2</a> - Useless file modification.</li>
<li><a href='#cs3'>CS3</a> - Binary file addition.</li>
</ul>
<a name='cs1'></a>
<table>
<tr><td><pre>Added test file.
</pre></td></tr>
<tr><td>A</td><td><font>2</font></td><td><font>trunk/README.txt</font></td></tr>
</table>
<pre>
<hr />
<font>--- /dev/null
+++ trunk/README.txt	(revision 2)
</font><font>+Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod
+tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim
+veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex
+ea commodi consequat. Quis aute iure reprehenderit in voluptate velit
+esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat
+cupiditat non proident, sunt in culpa qui officia deserunt mollit anim
+id est laborum.
</font></pre>
<p>&nbsp;</p>
<a name='cs2'></a>
<table>
<tr><td><pre>Useless file modification.
</pre></td></tr>
<tr><td>M</td><td>3</td><td>trunk/README.txt</td></tr>
</table>
<pre>
<hr />
<font>--- trunk/README.txt	(revision 2)
+++ trunk/README.txt	(revision 3)
</font><font>@@ -1,7 +1,4 @@
</font><font>-Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod
</font><font>+  Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod
</font> tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim
 veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex
<font>-ea commodi consequat. Quis aute iure reprehenderit in voluptate velit
-esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat
-cupiditat non proident, sunt in culpa qui officia deserunt mollit anim
-id est laborum.
</font><font>+ea commodi consequat.
</font></pre>
<p>&nbsp;</p>
<a name='cs3'></a>
<table>
<tr><td><pre>Binary file addition.
</pre></td></tr>
<tr><td>A</td><td><font>4</font></td><td>[BIN] <font>trunk/random.dat</font></td></tr>
</table>
<p>&nbsp;</p>

""")

class TestSvnViewvc(TestHtml):
    repository_name = 'module.svn'
    template_path = 'test/repository/module.svn.dump'
    repository_module = 'module_a',

    # test ViewVc link
    def testViewVc(self):
        self.assertHtmlEqual(self.runDli(start_revision=1, end_revision=2,
                                         show_text=False, show_html=True,
                                         web_url='http://foo.svn.sf.net/viewvc/foo'),
                             """<body>
<h3>ChangeSet Index:</h3>
<ul>
<li><a href='#cs1'>CS1</a> - File in module a.</li>
</ul>
<a name='cs1'></a>
<table>
<tr><td><pre>File in module a.
</pre></td></tr>
<tr><td><a href="http://foo.svn.sf.net/viewvc/foo/module_a/trunk/file_a?rev=2&amp;content-type=text/vnd.viewcvs-markup">A</a></td><td><font>2</font></td><td><font>module_a/trunk/file_a</font></td></tr>
</table>
<pre>
<hr />
<font>--- /dev/null
+++ module_a/trunk/file_a	(revision 2)
</font><font>+file_a
</font></pre>
<p>&nbsp;</p>

""")

class TestGitHtml(TestHtml):
    repository_name = 'latin1.git'
    repository_type = 'git'
    template_path = 'test/repository/latin1.git.dump'

    # test bugzillate
    def testBugzillate(self):
        self.assertHtmlEqual(self.runDli(start_revision='30fbdf49',
                                         end_revision='aaa1319c',
                                         show_text=False, show_html=True),
                             u"""<body>
<h3>ChangeSet Index:</h3>
<ul>
<li><a href='#cs1'>CS1</a> - Fixed <a href='https://www.develer.com/bugs/show_bug.cgi?id=1234'>bug #1234</a>.</li>
</ul>
<a name='cs1'></a>
<table>
<tr><td><pre>Fixed <a href='https://www.develer.com/bugs/show_bug.cgi?id=1234'>bug #1234</a>.
</pre></td></tr>
<tr><td>M</td><td>aaa1319c1cd652ad8df995067c678e81803fc839</td><td>test_latin1.txt</td></tr>
</table>
<pre>
<hr />
<font>--- a/test_latin1.txt
+++ b/test_latin1.txt
</font><font>@@ -1 +1 @@
</font><font>-Another test latin1 àèìòù.
</font><font>+Test bugzillate.
</font></pre>
<p>&nbsp;</p>

""")

class TestDiffSpecial(TestHtml):
    repository_name = 'special.svn'
    template_path = 'test/repository/special.svn.dump'

    def testUTF(self):
        self.assertHtmlEqual(self.runDli(start_revision=0, end_revision=1,
                                         show_text=False, show_html=True),
                             """<body>
<h3>ChangeSet Index:</h3>
<ul>
<li><a href='#cs1'>CS1</a> - Added UTF-8 file.</li>
</ul>
<a name='cs1'></a>
<table>
<tr><td><pre>Added UTF-8 file.
</pre></td></tr>
<tr><td>A</td><td><font>1</font></td><td><font>foo-utf8.txt</font></td></tr>
</table>
<pre>
<hr />
<font>--- /dev/null
+++ foo-utf8.txt	(revision 1)
</font><font>+<span style="background-color: #FF0000">&lt;UTF-8 BOM&gt;</span>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt
</font></pre>
<p>&nbsp;</p>

""")

if __name__ == '__main__':
    unittest.main()
