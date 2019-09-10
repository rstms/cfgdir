import pytest
import sys
import json
from click.testing import CliRunner
from cfgdir import cli
from pprint import pprint

def _cli(args, config):
    print('_cli%s' % repr((args, config)))
    runner = CliRunner()
    result = runner.invoke(cli, args, catch_exceptions=False)
    assert result.exit_code == 0
    assert result.output 
    print(result.output)
    cfg = json.loads(result.output)
    assert type(cfg)==dict
    assert cfg == config
    #pprint(cfg)

def test_cli():
    _cli(['tests/data/cfg'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo'})
    _cli(['tests/data/cfg1'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo'})
    _cli(['tests/data/cfg2'], {'KEY_1':'1', 'KEY_3': '3'})

def test_types():
    _cli(['tests/data/cfg3'], {'KEY_1':1, 'KEY_2':2, 'KEY_3': 'foo'})

def test_recurse():
    _cli(['tests/data/cfg1', '-r'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo', 'sub': {'V1':'value'}})

def test_recurse_compact():
    _cli(['tests/data/cfg1', '-r', '-c'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo', 'sub': {'V1':'value'}})

def test_lf_data():
    _cli(['tests/data/cfg4'], {'LF_VALUE': '', 'LFINT': None})

