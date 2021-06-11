#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 01-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""
from pathlib import Path
from doit.action import CmdAction
from doit.tools import config_changed

from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
template_files = list(Path('templates').glob('*.xmds'))
env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)


def render_template(template_name, output_name, conf):
    template = env.get_template(template_name)
    output = template.render(conf=conf)
    with open(output_name, 'w') as f:
        f.write(output)


# rudimental task creators
# So I avoid to write the render - compile - run loop twice
def create_render_task(name, build_path, conf):
    template = f"{name}.xmds"
    script = build_path / template
    return {
        'name': 'render',
        'actions': [(render_template, (template, script, conf))],
        'uptodate': [config_changed(conf)],
        'file_dep': template_files,
        'targets': [script]
    }


def create_compile_task(name, build_path):
    return {
        'name': 'compile',
        'actions': [CmdAction(f"xmds2 {name}.xmds", cwd=build_path)],
        'file_dep': [build_path / f"{name}.xmds"],
        'targets': [build_path / f"{name}"]
    }


def create_run_task(name, build_path, output_filename, init_filename=None):
    filedeps = [name, init_filename] if init_filename is not None else [name]
    return {
        'name': 'run',
        'actions': [CmdAction(f"./{name}", cwd=build_path)],
        'file_dep': [build_path / _name for _name in filedeps],
        'targets': [build_path / output_filename]
    }
