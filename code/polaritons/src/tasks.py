#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 01-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
import signal
from pathlib import Path
from doit.action import CmdAction
from doit.tools import config_changed

import collections.abc
from copy import deepcopy

from jinja2 import Environment, FileSystemLoader


def preexec_function():
    signal.signal(signal.SIGHUP, signal.SIG_IGN)


file_loader = FileSystemLoader('templates')
template_files = list(Path('templates').glob('*.xmds'))
env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)


def conf_update(conf, name):
    _conf = deepcopy(conf)
    _conf['exec_filename'] = name
    return rec_update(_conf, _conf[name])


def rec_update(d, u):
    # recursive dict update
    # https://stackoverflow.com/a/3233356
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = rec_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def render_template(template_name, output_name, conf):
    template = env.get_template(template_name)
    output = template.render(conf=conf)
    with open(output_name, 'w') as f:
        f.write(output)


def xmds_run(build_dir, conf, h5filepath=None):
    """Mandatory keys in conf:
        exec_filename: name of the xmds script
        output_filename: target h5file
    """
    name = conf['exec_filename']
    output_filename = conf['output_filename']
    init_filename = conf.get('init_filename', None)
    yield create_render_task(name, build_dir, conf)
    yield create_compile_task(name, build_dir)
    yield create_run_task(name, build_dir, output_filename, init_filename)


# rudimental task creators
# So I avoid to write the render - compile - run loop twice
def create_render_task(name, build_dir, conf):
    template = f"{name}.xmds"
    script = build_dir / template
    return {
        'name': 'render',
        'actions': [(render_template, (template, script, conf))],
        'uptodate': [config_changed(conf)],
        'file_dep': template_files,
        'targets': [script]
    }


def create_compile_task(name, build_dir):
    return {
        'name': 'compile',
        'actions': [CmdAction(f"wsl xmds2 {name}.xmds", cwd=build_dir)],
        'file_dep': [build_dir / f"{name}.xmds"],
        'targets': [build_dir / f"{name}"]
    }


def create_run_task(name, build_dir, output_filename, init_filename=None):
    filedeps = [f"{name}.exe", init_filename] if init_filename is not None else [name]
    return {
        'name': 'run',
        # 'actions': [CmdAction(f"mpirun -n 24 ./{name} | tee {name}.log", cwd=build_dir)],
        'actions': [CmdAction(f"wsl ./{name} | wsl tee {name}.log", cwd=build_dir)],
        'file_dep': [build_dir / _name for _name in filedeps],
        'targets': [build_dir / output_filename]
    }
