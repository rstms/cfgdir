# cfgdir
Read envdir style configuration directory and output as JSON

I'm a long-time fan of DJB's [envdir](https://cr.yp.to/daemontools/envdir.html)

I'm pleased by the simple power of using the filesystem as your database, and the
freedom to manipulate the configuration data in any way one choses.

Rather than running another program with the configuration in environment variables,
this program outputs a stream in JSON format.  This output can be captured in a file
or piped into stdin of another program.

## Interface

~~~
cfgdir d
~~~

reads a JSON object from stdin, then reads the directory named d, outputting a JSON object modified according to files in d.  

The format of d is as follows: (adapted from envdir's documentation) 
> If d contains a file named s whose first line is t, cfgdir's output will contain an element named s with string value t. The name s must not contain =. Spaces and tabs at the end of t are removed. Nulls in t are changed to newlines.  
> If the file s is completely empty (0 bytes long) cfgdir will remove the element named s if it exists.
