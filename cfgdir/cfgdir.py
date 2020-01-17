#!/usr/bin/env python

import click
import os
import json as lib_json
import yaml as lib_yaml
import sys

from .version import VERSION

@click.command()
@click.option('-c', '--compact', is_flag=True, help='minimize output')
@click.option('-s', '--sort', is_flag=True, help='sort output')
@click.option('-j', '--json', is_flag=True, default=False, help='JSON format')
@click.option('-y', '--yaml', is_flag=True, default=False, help='YAML format')
@click.option('-e', '--dotenv', is_flag=True, default=False, help='.env format')
@click.option('-r', '--recurse', is_flag=True, default=False,
              help='process subdirectories')
@click.option('-o', '--overlay', default='',
              help='overlay JSON/YAML string onto output')
@click.argument('directory', type=click.Path(exists=True, file_okay=False),
                default=os.devnull)  # , help='directory containing configuration values')
@click.argument('input', type=click.File('rb'),
                default=os.devnull)  # , help='optional input filename or - for stdin, defaults to none')
@click.argument('output', type=click.File('wb'), default='-')  # , help='optional output filename')
@click.version_option(VERSION)
def cli(directory, input, output, compact, sort, json, yaml, dotenv, recurse, overlay):

    default = input.read()

    if yaml:
        parser = lib_yaml.safe_load
    elif dotenv:
        parser = dotenv_load
    else:
        parser = lib_json.loads
    if default:
        cfg = parser(default)
    else:
        cfg = {}
    cfg = read_dir_as_dict(directory, cfg, recurse)

    if overlay:
        cfg = apply_overlay(cfg, parser(overlay))

    if compact:
        i = None
        s = (',', ':')
    else:
        i = 2
        s = (',', ': ')
    if yaml:
        out = lib_yaml.dump(cfg)
    elif dotenv:
        out = dotenv_dump(cfg, sort)
    else:
        out = lib_json.dumps(cfg, sort_keys=sort, indent=i, separators=s)
    output.write((out + '\n').encode('utf-8'))
    output.flush()

def _null(s):
    return None

def read_file_value(filename, key):
    with open(filename) as f:
        value = f.readline().strip()

    if value:
        while value[-1] in ('\n', ' ', '\t'):
            value = value[:-1]

    (key, value) = apply_type_conversion(key, value)

    # convert nulls in string to newlines
    if type(value) == str:
        value = ''.join(['\n' if c == '\0' else c for c in value])

    return (key, value)


def convert_bool(value):
    value = value.strip().lower()
    if value in ['', '0', 'false', 'f', 'no', 'n']:
        value = False
    else:
        value = True
    return value


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
        ('.boolean', convert_bool),
        ('.bool', convert_bool),
        ('.b', convert_bool),
        ('.null', _null),
    ]
    for extension, convert in type_conversions:
        if key.endswith(extension):
            key = key[:-len(extension)]
            value = convert(value) if value else None
            break
    return key, value


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
                    del (result[f])
        if recurse:
            for d in dirs:
                result[d] = read_dir_as_dict(os.path.join(name, d),
                                             result.setdefault(d, {}), recurse)
        break
    return result

def apply_overlay(source, overlay):
    """apply add keys from overlay into source"""
    for k, v in overlay.items():
        if type(v) == dict:
            source.setdefault(k, {})
            source[k] = apply_overlay(source[k], overlay[k])
        else:
            source[k] = v
    return source

def dotenv_load(data_str):
  ret = {}
  for l in data_str.split('\n'):
    a=l.split('=')
    ret[a[0]]='='.join(a[1:])
  return ret

def dotenv_dump(data_dict, sort=False):
  ret = ''
  for k,v in data_dict.items():
    ret = '%s%s%s' % (ret, '\n' if len(ret) else '', '%s=%s' % (k, v))
  if sort:
    ret = '\n'.join(sorted(ret.split('\n')))
    
  return ret

if __name__=='__main__':
    cli(sys.argv[1:])
