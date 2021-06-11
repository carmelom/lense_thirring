#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: 01-1970 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""
Module docstring

"""

import h5py


def recursive_read_attrs(h5filename, group):
    def _read(group, d):
        d.update(dict(group.attrs))
        for key in group.keys():
            # if isinstance(group[key], h5py.Group):
            d[key] = {}
            _read(group[key], d[key])

    d = {}

    with h5py.File(h5filename, 'r') as f:
        _read(f[group], d)

    return d


def load_vortices(h5filename, home_group):
    with h5py.File(h5filename, 'r') as f:
        has_vortices = 'vortices' in f[home_group]

    recompute = False

    if has_vortices and not recompute:
        print('re-read')
        vortices = {}

        with h5py.File(h5filename, 'r') as f:
            g = f[f'{home_group}/vortices']
            rmin = g.attrs['rmin']
            rmax = g.attrs['rmax']
            threshold_distance = g.attrs['threshold_distance']
            for key in g.keys():
                uid = int(key)
                vg = g[key]
                vx = {'time': vg['time'][:], 'coords': vg['coords'][:]}
                vortices[uid] = vx

    else:
        rmin, rmax = 7, 40
        threshold_distance = 0.4

        vortices = tracker.vortex_tracker(x, y, t, psiR, psiI, cutoff_radii=(rmin, rmax), threshold_distance=threshold_distance)

        with h5py.File(h5filename, 'a') as f:
            g = f.require_group(f'{home_group}/vortices')
            g.attrs['rmin'] = rmin
            g.attrs['rmax'] = rmax
            g.attrs['threshold_distance'] = threshold_distance
            for uid, vx in vortices.items():
                vg = g.require_group(f"{uid:03d}")
                vg['time'] = vx['time']
                vg['coords'] = vx['coords']
