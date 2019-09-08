import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cfgdir-rstms",
    version="0.0.1",
    author="Matt Krueger",
    author_email="mkrueger@rstms.net",
    description="output envdir as JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rstms/cfgdir",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",

    ],
    #python_requires='>=3.6',
    py_modules=['cfgdir'],
    include_package_data=True,
    install_requires=[
        'Click',
        'pyyaml',
   ],
   entry_points='''
       [console_scripts]
           cfgdir=cfgdir:cli
   ''',
)
