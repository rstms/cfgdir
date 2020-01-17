from setuptools import setup, find_packages
from glob import glob
from os.path import basename, splitext

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('VERSION', 'r') as fh:
    version = fh.readline().strip()

with open('requirements.txt', 'r') as fh:
    requires = [l.strip() for l in fh.readlines()]

setup(
    name="cfgdir",
    version=version,
    author="Matt Krueger",
    author_email="mkrueger@rstms.net",
    description="output envdir as JSON or YAML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/rstms/cfgdir",
    keywords='envdir configuration config',
    packages=find_packages(exclude=('tests', 'docs')),
    data_files=[('.', ['VERSION', 'LICENSE', 'requirements.txt'])],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    install_requires=requires,
    tests_require=['pytest', 'pytest-datadir'],
    entry_points={
        'console_scripts': [
            'cfgdir=cfgdir:cli',
        ],
    },
)
