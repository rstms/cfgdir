import pytest
import sys
import json
from click.testing import CliRunner
from cfgdir import cli
from pprint import pprint

def _cli(args, config):
    print('_cli%s' % repr((args, config)))
    runner = CliRunner()
    result = runner.invoke(cli, args)
    if result.exception:
        raise result.exception
    assert result.exit_code == 0
    assert result.output 

    cfg = json.loads(result.output)
    assert type(cfg)==dict
    assert cfg == config
    pprint(cfg)

def test_cli():
    _cli(['../test/cfg'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo'})
    _cli(['../test/cfg1'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo'})
    _cli(['../test/cfg1', '-r'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo', 'sub': {'V1':'value'}})
    _cli(['../test/cfg1', '-r', '-c'], {'KEY_1':'1', 'KEY_2':'2', 'KEY_3': 'foo', 'sub': {'V1':'value'}})
    _cli(['../test/cfg2'], {'KEY_1':'1', 'KEY_3': '3'})
    _cli(['../test/cfg3'], {'KEY_1':1, 'KEY_2':2, 'KEY_3': 'foo'})
