#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 06-2019 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

import h5py


def plot_wavefunction(h5filename, group=''):
    with h5py.File(h5filename, 'r') as f:
        g = f[f"{group}/1"]
        x = g['x'][:]
        y = g['x'][:]
        psiI = g['psiI'][:]
        psiR = g['psiR'][:]

    R_tf = 4.2

    density = psiR**2 + psiI**2
    phase = np.arctan2(psiR, psiI)

    if len(density.shape) == 3:
        density = density[0]
        phase = phase[0]

    extent = (x.min(), x.max(), y.min(), y.max())

    h, w = plt.rcParams['figure.figsize']
    fig, (ax, ax_p) = plt.subplots(1, 2, figsize=(2 * w, h), sharey=True)
    fig.suptitle(h5filename)

    kk = {'ticks': None, 'orientation': 'horizontal',
          'ticklocation': 'top'}  # read this from make_axes

    c1 = ax.imshow(density, extent=extent, vmin=0, vmax=density.max())
    cax = ax.inset_axes([0, 1.06, 1, 0.04])
    plt.colorbar(c1, cax, **kk)

    c2 = ax_p.imshow(phase, cmap='RdBu', extent=extent)
    cax = ax_p.inset_axes([0, 1.06, 1, 0.04])
    plt.colorbar(c2, cax, **kk)

    for _ax, col in zip((ax, ax_p), ('w', 'k')):
        e = Ellipse((0, 0), 2 * R_tf, 2 * R_tf,
                    ls='--', lw=0.3, ec=col, fc='none')
        _ax.add_patch(e)

    R = abs(x.min())
    ax.set(xlim=(-R, R), ylim=(-R, R))
    ax_p.set(xlim=(-R, R), ylim=(-R, R))
    plt.show()


if __name__ == '__main__':
    plot_wavefunction('build/groundstate_full.h5')
