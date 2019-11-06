import json
import yaml

from click.testing import CliRunner

import cfgdir


def test_init():
    cli = cfgdir.cli
    assert cli

def test_call():
    #result = cfgdir.cli()
    #assert result
    assert True

def _cli(args, config, parse_yaml=False):

    print('_cli%s' % repr((args, config)))
    runner = CliRunner()
    result = runner.invoke(cfgdir.cli, args, catch_exceptions=True)
    assert result.output
    print('results:\n%s' % result.output)
    assert result.exit_code == 0
    if parse_yaml:
        cfg = yaml.safe_load(result.output)
    else:
        cfg = json.loads(result.output)
    assert type(cfg) == dict
    assert cfg == config
    # pprint(cfg)


def test_cli(datadir):
    _cli([str(datadir / 'cfg')], {'KEY_1': '1', 'KEY_2': '2', 'KEY_3': 'foo'})
    _cli([str(datadir / 'cfg1')], {'KEY_1': '1', 'KEY_2': '2', 'KEY_3': 'foo'})
    _cli([str(datadir / 'cfg2')], {'KEY_1': '1', 'KEY_3': '3'})


def test_types(datadir):
    _cli([str(datadir / 'cfg3')],
         {'KEY_1': 1, 'KEY_2': 2, 'KEY_3': 'foo', 'b1': True,
          'b2': False, 'b3': True, 'b4': False, 'b5': False})


def test_recurse(datadir):
    _cli([str(datadir / 'cfg1'), '-r'],
         {'KEY_1': '1', 'KEY_2': '2', 'KEY_3': 'foo', 'sub': {'V1': 'value'}})


def test_recurse_compact(datadir):
    _cli([str(datadir / 'cfg1'), '-r', '-c'],
         {'KEY_1': '1', 'KEY_2': '2', 'KEY_3': 'foo', 'sub': {'V1': 'value'}})


def test_lf_data(datadir):
    _cli([str(datadir / 'cfg4')], {'LF_VALUE': '', 'LFINT': None})


def test_yaml_switch(datadir):
    _cli(
        [str(datadir / 'cfg'), '-y'],
        {'KEY_1': '1', 'KEY_2': '2', 'KEY_3': 'foo'},
        parse_yaml=True)


def test_json_switch(datadir):
    _cli([str(datadir / 'cfg'), '-j'],
         {'KEY_1': '1', 'KEY_2': '2', 'KEY_3': 'foo'})


def test_overwrite(datadir):
    _cli([str(datadir / 'cfg5'), str(datadir / 'default.json')],
         {'KEY_1': '1_over', 'KEY_2': '2', 'KEY_3': 'foo.over'})


def test_recurse_overwrite(datadir):
    results = {
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
    _cli([str(datadir / 'cfg6'), str(datadir / 'default6.json'), '-r'], results)


def test_overlay(datadir):
    results = {
        "KEY_1": "1_over",
        "KEY_2": "over2",
        "sub": {
            "V1": "newvalue",
            "NEWBOOL": False,
            "NEWKEY": 1,
            "SUB2": "subover2"
        },
        "KEY_3": "foo.over"
    }

    o = '{"KEY_2":"over2", "sub": {"SUB2":"subover2"}}'
    j = json.loads(o)
    assert j
    assert type(j) == dict
    assert j == {'KEY_2': 'over2', 'sub': {'SUB2': 'subover2'}}
    _cli([str(datadir / 'cfg7'), '-r', '-o', o], results)
