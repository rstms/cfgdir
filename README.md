# cfgdir
Read envdir style configuration directory and output as JSON

Project is hosted at https://github.com/rstms/cfgdir

Inspired by djb's excellent [envdir](https://cr.yp.to/daemontools/envdir.html)

Leverage the powerful simplicity of the filesystem as your configuration database, and the
freedom to fluidly manipulate configuration data from your shell.

Unlike envdir's mechanism of running another program with the configuration in environment variables,
this program outputs a stream in JSON or YAML format.  This output can be captured in a file
or piped into stdin of another program.

## Interface

~~~
cfgdir [OPTIONS] d [INPUT] [OUTPUT]
~~~

optionally reads a JSON or YAML object from INPUT (use - to read stdin) , then reads the directory named d, outputting a JSON or YAML object modified according to files in d.  

The format of d is as follows: (adapted from envdir's documentation) 
> If d contains a file named s whose first line is t, cfgdir's output will contain an element named s with string value t. The name s must not contain =. Spaces and tabs at the end of t are removed. Nulls in t are changed to newlines.  
> If the file s is completely empty (0 bytes long) cfgdir will remove the element named s if it exists.


### Arguments:
   ----------|----------|--|----------
   DIRECTORY | required | | Directory containing configuration data files
   INPUT | optional | /dev/null | Input filename or - for stdin
   OUPUT | optional | stdout | Output Filename or - for stdout

### Options:
```
  -c, --compact  minimize output
  -s, --sort     sort output
  -j, --json     JSON format
  -y, --yaml     YAML format
  -r, --recurse  process subdirectories
  --help         Show this message and exit.
```
