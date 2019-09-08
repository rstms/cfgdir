# python package makefile

PROJECT:=cfgdir

# prefer python3
PYTHON:=python3

.PHONY: help tools install uninstall dist publish

help: 
	@echo "make tools|install|uninstall|dist|publish"

tools: 
	${PYTHON} -m pip install --user --upgrade setuptools wheel twine

install:
	@echo Installing ${PROJECT} locally
	${PYTHON} -m pip install --user --upgrade .

uninstall: 
	@echo Uninstalling ${PROJECT} locally
	${PYTHON} -m pip uninstall -y ${PROJECT} 

clean:
	@echo Cleaning up...
	rm -rf build dist *.egg-info

dist:
	@echo building ${PROJECT}
	${PYTHON} setup.py sdist bdist_wheel

publish: dist
	@echo publishing ${PROJECT} to PyPI
	${PYTHON} -m twine upload dist/*
