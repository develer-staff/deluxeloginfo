all:
	@echo "make [test|test_launcher|testcover|clean]"

test:
	python test/test.py

test_launcher:
	 PYTHONPATH=. python test/LauncherTest.py

testcover:
	PERL5OPT=-MDevel::Cover python test/test.py
	cover

clean:
	rm -rf cover_db
	rm -rf test/stamps/*
	rm -rf test/tmp/*
	rm -rf test/repository/*.svn
	rm -rf test/repository/*.git
	rm -rf test/repository/*.hg

.PHONY: all test testcover clean

