#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 01-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
import h5py
from pathlib import Path
from src import tasks
from src import h5tools
from src.read_log import read_log
from doit import get_var

from ruamel import yaml

TO_RUN = [
    'realtime'
]

DOIT_CONFIG = {
    'verbosity': 2,
    'backend': 'json',
    'default_tasks': TO_RUN + ['collect'],
    'dep_file': '.doit1.db',
}

config_file = get_var('config_file', 'configure.yaml')

with open(config_file, 'r') as f:
    conf = yaml.safe_load(f)


build_dir = Path(conf['build_dir'])
build_dir.mkdir(parents=True, exist_ok=True)

run_dir = Path(conf['run_dir'])

sequence_index = int(get_var('sequence_index', h5tools.autosequence(run_dir)))
run_number = int(get_var('run_number', 0))

h5filepath = run_dir / \
    conf['h5filepath'].format(
        sequence_index=sequence_index, run_number=run_number)


def task_realtime():
    name = 'realtime'
    _conf = tasks.conf_update(conf, name)
    return tasks.xmds_run(build_dir, _conf)


def task_collect():
    actions = [(h5tools.mkpath, [h5filepath, conf])]
    fdeps = []

    def _log(name):
        log_results = read_log(build_dir / f"{name}.log")
        h5tools.save_data(h5filepath, log_results, group=f'{name}/log')
        with open(build_dir / f"{name}.log", 'r') as f:
            logfile = f.read()
        with h5py.File(h5filepath, 'a') as h5file:
            h5file[f"{name}/log/logfile"] = logfile

    for name in TO_RUN:
        target_file = build_dir / conf[name]['output_filename']
        actions.append((h5tools.copy_group, [target_file, h5filepath, name]))
        actions.append((_log, [name]))
        fdeps.append(target_file)

    return {
        'actions': actions,
        'file_dep': fdeps
    }
