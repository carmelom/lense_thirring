#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: 05-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path

DOIT_CONFIG = {
    'verbosity': 2,
    'default_tasks': []
}

source = Path('./')
host = 'shin'
dest = '/home/carmelo/lense_thirring'

excluded = [
    'lense-thirring.md',
    '**/build',
    '**/.*',
    '**/__pycache__'
]


def task_push():
    cmd = ['rsync', '-avh']
    cmd += [f'--exclude {path}' for ex in excluded for path in source.glob(ex)]
    cmd += [str(source), f"{host}:{dest}"]
    cmd = ' '.join(cmd)
    return {
        # 'actions': [f"echo '{cmd}'"]
        'actions': [cmd]
    }
