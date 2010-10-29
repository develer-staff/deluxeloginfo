UPDATING DUMP FILES:

Subversion:
$ svnadmin dump ./svnrepo.svn > svnrepo.svn.dump

Git:
$ git --git-dir gitrepo.git fast-export --all > gitrepo.git.dump

Mercurial:
$ hg -R hgrepo bundle -a special.hg
