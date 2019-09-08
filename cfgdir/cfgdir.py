#!/usr/bin/env python

import click
import os
import json as lib_json
import yaml as lib_yaml

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

def read_file_value(filename):
    with open(filename) as f:
        value = f.readline()
    if value.endswith('\n'):
        value = value[:-1]
    return value
       
def read_dir_as_dict(directory, result, recurse):
    for name, dirs, files in os.walk(directory):
        for f in files:
            pathname = os.path.join(name, f)
            if os.path.getsize(pathname):
                result[f] = read_file_value(pathname)
            else:
                if f in result:
                    del(result[f])
        if recurse:
            for d in dirs:
                result[d] = read_dir_as_dict(os.path.join(name, d), {}, recurse)
        break
    return result

