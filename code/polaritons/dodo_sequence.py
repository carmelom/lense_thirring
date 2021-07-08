#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: 07-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
import itertools
from copy import deepcopy
from src.h5tools import autosequence

from ruamel import yaml

DOIT_CONFIG = {
    'verbosity': 2,
    'backend': 'json',
    'dep_file': '.doit.db',
}


with open('configure.yaml', 'r') as f:
    conf = yaml.safe_load(f)

run_dir = Path(conf['run_dir'])
run_dir.mkdir(parents=True, exist_ok=True)
sequence_index = autosequence(run_dir)

# scan = {
#     'nu': [20, 15],
# }
#
# keys, values = list(zip(*scan.items()))
#
# shots = []
# for item in itertools.product(*values):
#     conf['globals'].update(dict(zip(keys, item)))
#     shots.append(deepcopy(conf))
c1 = deepcopy(conf)
c1['imprint_pair']['globals']['v1'] = 1
c1['imprint_pair']['globals']['v2'] = -1

c2 = deepcopy(conf)
c2['imprint_pair']['globals']['v1'] = -1
c2['imprint_pair']['globals']['v2'] = 1

shots = [c1, c2]


def task_run_sequence():
    def _write_conf(_conf, filename):
        # print("WRITING")
        # pprint(_conf)
        with open(filename, 'w') as f:
            f.write(yaml.safe_dump(_conf))

    for j, conf in enumerate(shots):
        conf_name = '_config.yaml'
        cmd = f"doit -f dodo.py config_file={conf_name} sequence_index={sequence_index} run_number={j}"
        yield {
            'name': j,
            'actions': [
                (_write_conf, [conf, conf_name]),
                cmd
                # f"nohup {cmd} & disown"
            ]
        }


# def task_clear():
#     return {
#         'actions': ['doit -f dodo.py clear']
#     }
