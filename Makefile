all:
	@echo "make [test|testcover|clean]"

test:
	python test/test.py

testcover:
	PERL5OPT=-MDevel::Cover python test/test.py
	cover

clean:
	rm -rf cover_db
	rm -rf test/stamps/*
	rm -rf test/tmp/*
	rm -rf test/repository/base.svn

.PHONY: all test testcover clean