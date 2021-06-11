#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 01-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
from movie2d import make_movie
import tasks


build_path = Path('build')
build_path.mkdir(parents=True, exist_ok=True)


DOIT_CONFIG = {
    'verbosity': 2,
    'backend': 'json',
    'default_tasks': [
        'groundstate',
        # 'realtime',
    ]
}

_globals = {
    'n0': 20,
    'nu': 1,
    'radius': 6,
    'U0': 100,
    # sink potential
    'Gamma': 10,
    'sigma': 1,
    # imaginary damping
    'Lambda': 0.1
}

runtime = 2
gs_runtime = 10
steps = 200

groundstate_output = "groundstate.h5"
realtime_output = "realtime.h5"


def task_groundstate():
    name = 'groundstate'
    conf = {
        'exec_filename': name,
        'output_filename': groundstate_output,
        'gs_runtime': gs_runtime,
        'globals': _globals
    }
    yield tasks.create_render_task(name, build_path, conf)
    yield tasks.create_compile_task(name, build_path)
    yield tasks.create_run_task(name, build_path, groundstate_output)


def task_realtime():
    name = 'realtime'
    init_filename = groundstate_output
    output_filename = realtime_output
    conf = {
        'exec_filename': name,
        'init_filename': init_filename,
        'output_filename': output_filename,
        'globals': _globals,
        'runtime': runtime, 'steps': steps
    }
    yield tasks.create_render_task(name, build_path, conf)
    yield tasks.create_compile_task(name, build_path)
    yield tasks.create_run_task(name, build_path, output_filename, init_filename)


def task_movie():
    # h5file = build_path / realtime_output
    h5file = build_path / 'groundstate_full.h5'
    # output = None
    output = 'movie.mp4'
    return {
        'actions': [(make_movie, [h5file, 20, output], {})]
    }
