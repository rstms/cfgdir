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

VERSION: ${SOURCES}
	scripts/bumpbuild >VERSION src/${PROJECT}/version.py ${VERSION}
	git commit -m "v`cat VERSION`" -a
	git push

dist: gitclean VERSION 
	@echo building ${PROJECT}
	${PYTHON} setup.py sdist bdist_wheel

publish: release
	@echo publishing ${PROJECT} v`cat VERSION` to PyPI
	${PYTHON} -m twine upload dist/*

release: dist
	TAG="v`cat VERSION`"; git tag -a $$TAG -m "Release $$TAG"; git push origin $$TAG

clean:
	@echo Cleaning up...
	rm -rf build dist src/*.egg-info .pytest_cache .tox tests/exif-samples
	find . -type d -name __pycache__ | xargs rm -rf
	find . -name '*.pyc' | xargs rm -f

