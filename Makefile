# python package makefile

PROJECT:=$(shell basename `pwd`)

# prefer python3
PYTHON:=python3

# find all python sources (used to determine when to bump build number)
SOURCES:=$(shell find setup.py Makefile src tests -name '*.py')

# if VERSION=major or VERSION=minor specified, 
$(if ${VERSION}, $(shell touch src/${PROJECT}/version.py))

.PHONY: help tools test install uninstall dist gitclean publish release clean 

help: 
	@echo "make tools|install|uninstall|test|dist|publish|release|clean"

tools: 
	${PYTHON} -m pip install --upgrade setuptools wheel twine tox pytest

TPARM :=

test:
	@echo "Testing..."
	pytest -vvx --no-print-logs $(TPARM)

install:
	@echo Installing ${PROJECT} locally
	${PYTHON} -m pip install --upgrade --editable .

uninstall: 
	@echo Uninstalling ${PROJECT} locally
	${PYTHON} -m pip uninstall -y ${PROJECT} 

gitclean: 
	$(if $(shell git status --porcelain), $(error "git status dirty, commit and push first"))

VERSION: gitclean ${SOURCES}
	# If VERSION=major|minor or sources have changed, bump corresponding version element
	# and commit after testing for any other uncommitted changes.
	scripts/bumpbuild >VERSION src/${PROJECT}/version.py ${VERSION}
	@echo "Version bumped to `cat VERSION`"
	@EXPECTED_STATUS=$$(/bin/echo -e " M VERSION\n M src/${PROJECT}/version.py");\
        if [ "`git status --porcelain`" != "$$EXPECTED_STATUS" ]; then \
	  echo "git state is dirty, not committing version update."; exit 1; \
	else \
	  echo "Committing version update..."; \
	  git add VERSION src/${PROJECT}/version.py; \
	  git commit -m "bumped version to `cat VERSION`"; \
	  git push; \
	fi

dist: VERSION 
	@echo building ${PROJECT}
	${PYTHON} setup.py sdist bdist_wheel

release: dist
	@echo pushing Release ${PROJECT} v`cat VERSION` to github...
	TAG="v`cat VERSION`"; git tag -a $$TAG -m "Release $$TAG"; git push origin $$TAG

# comment out following target if not publishing to PyPI
publish: release
	@echo publishing ${PROJECT} v`cat VERSION` to PyPI...
	${PYTHON} -m twine upload dist/*

clean:
	@echo Cleaning up...
	rm -rf build dist src/*.egg-info .pytest_cache .tox
	find . -type d -name __pycache__ | xargs rm -rf
	find . -name '*.pyc' | xargs rm -f
