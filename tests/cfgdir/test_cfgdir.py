import pytest
import sys
import json
import yaml
from click.testing import CliRunner
from cfgdir import cli
from pprint import pprint

def _cli(args, config, parse_yaml=False):
    print('_cli%s' % repr((args, config)))
    runner = CliRunner()
    result = runner.invoke(cli, args, catch_exceptions=False)
    assert result.exit_code == 0
    assert result.output 
    print('results:\n%s' % result.output)
    if parse_yaml:
        cfg = yaml.safe_load(result.output)
    else:
        cfg = json.loads(result.output)
    assert type(cfg)==dict
    assert cfg == config
    #pprint(cfg)

def test_cli():
    _cli(['tests/data/cfg'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo'})
    _cli(['tests/data/cfg1'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo'})
    _cli(['tests/data/cfg2'], {'KEY_1':'1', 'KEY_3': '3'})

def test_types():
    _cli(['tests/data/cfg3'], {'KEY_1':1, 'KEY_2':2, 'KEY_3': 'foo', 'b1': True,
    'b2':False, 'b3':True, 'b4': False, 'b5': False})

def test_recurse():
    _cli(['tests/data/cfg1', '-r'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo', 'sub': {'V1':'value'}})

def test_recurse_compact():
    _cli(['tests/data/cfg1', '-r', '-c'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo', 'sub': {'V1':'value'}})

def test_lf_data():
    _cli(['tests/data/cfg4'], {'LF_VALUE': '', 'LFINT': None})

def test_yaml_switch():
    _cli(
        ['tests/data/cfg', '-y'], 
        {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo'},
        parse_yaml=True)

def test_json_switch():
    _cli(['tests/data/cfg', '-j'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo'})

def test_overwrite():
    _cli(['tests/data/cfg5', 'tests/data/default.json'], {'KEY_1':'1_over', 'KEY_2':'2', 'KEY_3': 'foo.over'})

def test_recurse_overwrite():
    results={
      'KEY_1': 1,
      'KEY_2': 2,
      'KEY_3': 'foo',
      'b1': True,
      'b2': False,
      'b3': True,
      'b4': False,
      'b5': False,
      'sub': {
        'V1': 'newvalue',
        'V2': 1.243, 
        'V3': 3.14159, 
        'NEWKEY': 1,
        'NEWBOOL': False
      }
    }
    _cli(['tests/data/cfg6', 'tests/data/default6.json', '-r'], results)

def test_overlay():
    results = {
        "KEY_1":"1_over",
        "KEY_2": "over2",
        "sub":{
            "V1":"newvalue",
            "NEWBOOL": False,
            "NEWKEY": 1,
            "SUB2": "subover2"
        },
        "KEY_3":"foo.over"
    }

    o = '{"KEY_2":"over2", "sub": {"SUB2":"subover2"}}'
    j = json.loads(o)
    assert j
    assert type(j)==dict
    assert j == {'KEY_2': 'over2', 'sub': {'SUB2': 'subover2'}}
    _cli(['tests/data/cfg7', '-r', '-o', o], results)
