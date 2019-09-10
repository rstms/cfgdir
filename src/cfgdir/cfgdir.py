#!/usr/bin/env python

import click
import os
import json as lib_json
import yaml as lib_yaml
import sys

@click.command()

@click.option('-c', '--compact', is_flag=True, help='minimize output')
@click.option('-s', '--sort', is_flag=True, help='sort output')
@click.option('-j', '--json', is_flag=True, default=True, help='JSON format')
@click.option('-y', '--yaml', is_flag=True, default=False, help='YAML format')
@click.option('-r', '--recurse', is_flag=True, default=False, help='process subdirectories')
@click.argument('directory', type=click.Path(exists=True, file_okay=False)) #, help='directory containing configuration values')
@click.argument('input', type=click.File('rb'), default='/dev/null') #, help='optional input filename or - for stdin, defaults to none')
@click.argument('output', type=click.File('wb'), default='-') #, help='optional output filename')

def cli(directory, input, output, compact, sort, json, yaml, recurse):
    default = input.read()
    if yaml:
        json=False
    if default:
        if json:
            cfg = lib_json.loads(default)
        else:
            cfg = lib_yaml.safe_load(default)
    else:
        cfg = {}
    cfg = read_dir_as_dict(directory, cfg, recurse)
    if compact:
        i=None
        s=(',',':')
    else:
        i=2
        s=(',',': ')
    if json:
        out =  lib_json.dumps(cfg, sort_keys=sort, indent=i, separators=s) 
    else:
        out =  lib_yaml.dump(cfg)
    output.write((out+'\n').encode('utf-8'))
    output.flush()

def _null(s):
    return None

def read_file_value(filename, key):

    _key = key
    with open(filename) as f:
        value = f.readline().strip()

    if value:
        while value[-1] in ('\n', ' ', '\t'):
            value = value[:-1]

    (key, value) = apply_type_conversion(key, value)         

    # convert nulls in string to newlines
    if type(value)==str:
        value = ''.join(['\n' if c=='\0' else c  for c in value])
    
    return (key, value)

def apply_type_conversion(key, value):
    # support json type specification with filename extensions
    type_conversions = [
        ('.string', str),
        ('.s', str),
        ('.integer', int),
        ('.i', int),
        ('.number', float),
        ('.n', float),
        ('.float', float),
        ('.f', float),
        ('.boolean', bool),
        ('.bool', bool),
        ('.b', bool),
        ('.null', _null),
    ]
    for extension, convert in type_conversions:
        if key.endswith(extension):
            key = key[:-len(extension)]
            value = convert(value) if value else None
            break
    return (key, value)

       
def read_dir_as_dict(directory, result, recurse):
    for name, dirs, files in os.walk(directory):
        for f in files:
            pathname = os.path.join(name, f)
            if os.path.getsize(pathname):
                (k, v) = read_file_value(pathname, f)
                result[k] = v
            else:
                (f, _) = apply_type_conversion(f, None)
                if f in result:
                    del(result[f])
        if recurse:
            for d in dirs:
                result[d] = read_dir_as_dict(os.path.join(name, d), {}, recurse)
        break
    return result

