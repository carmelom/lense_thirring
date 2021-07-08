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
import lmfit
from ruamel import yaml

with open('configure.yaml', 'r') as f:
    conf = yaml.safe_load(f)
globs = conf['globals']


def gs_wavefunction(x, y, zeta, nu, alpha):
    r = np.hypot(x, y)
    phi = np.arctan2(x, y)
    psi = np.sqrt(1 / alpha) * np.maximum(0, 1 - (nu**2 + zeta**2) / (r**2 + 1e-3)) * np.exp(1j * (zeta * np.log(r + 1e-3) + nu * phi))
    # return np.where(np.isfinite(psi), psi, 0)
    return psi


def plot_gs(h5filename, group=''):
    with h5py.File(h5filename, 'r') as f:
        g = f[f"{group}/1"]
        t = g['t'][:]
        x = g['x'][:]
        y = g['x'][:]
        psiI = g['psiI'][:]
        psiR = g['psiR'][:]

    R_tf = 4.2

    density = psiR**2 + psiI**2
    phase = np.arctan2(psiR, psiI)

    psi = psiR + 1j * psiI

    n0 = density[-1]
    p0 = phase[-1]

    r = x[len(x) // 2:]
    radial_slice = np.index_exp[:, len(x) // 2, len(x) // 2:]

    extent = (x.min(), x.max(), y.min(), y.max())

    h, w = plt.rcParams['figure.figsize']
    h *= 0.8
    fig, (ax, ax_p) = plt.subplots(1, 2, figsize=(2 * w, h), sharey=True)
    fig.suptitle(h5filename)

    kk = {'ticks': None, 'orientation': 'horizontal',
          'ticklocation': 'top'}  # read this from make_axes

    c1 = ax.imshow(n0, extent=extent)
    cax = ax.inset_axes([0, 1.06, 1, 0.04])
    plt.colorbar(c1, cax, **kk)

    c2 = ax_p.imshow(p0, cmap='RdBu', extent=extent)
    cax = ax_p.inset_axes([0, 1.06, 1, 0.04])
    plt.colorbar(c2, cax, **kk)

    R = abs(x.min())
    ax.set(xlim=(-R, R), ylim=(-R, R))
    ax_p.set(xlim=(-R, R), ylim=(-R, R))

    fig, (ax, ax1, ax3) = plt.subplots(1, 3, figsize=(3 * w, h))
    ax.plot(r, density[radial_slice][0], 'C1--')
    ax.plot(r, density[radial_slice][-1])
    alpha = globs['alpha']
    ax.axhline(1 / alpha)

    # fit wf
    psi0 = psi[-1]
    M = lmfit.Model(gs_wavefunction, independent_vars=['x', 'y'], nan_policy='omit')
    M.set_param_hint('zeta', min=0)
    M.set_param_hint('nu', min=0)
    M.set_param_hint('alpha', min=0)
    X, Y = np.meshgrid(x, y)
    R = np.hypot(X, Y)

    where = (R < 11) & (R > 1.5)
    to_fit = psi0.copy()
    # to_fit[~where] = np.nan

    p0 = M.make_params(zeta=10, nu=1, alpha=1e-3)

    res = M.fit(to_fit, p0, x=X, y=Y)
    print(res.fit_report())
    psi_fit = gs_wavefunction(X, Y, **res.params.valuesdict())
    n0 = abs(psi_fit[radial_slice[1:]])**2
    p0 = np.angle(psi_fit)[radial_slice[1:]]


    ax.plot(r, n0, 'C3')

    ax1.plot(r, phase[radial_slice][0], 'C1--')
    ax1.plot(r, phase[radial_slice][-1])

    ax1.plot(r, p0, 'C3')

    norm = density.sum(axis=(1, 2))
    ax3.plot(t, norm)

    fig, (ax, ax_p) = plt.subplots(1, 2, figsize=(2 * w, h), sharey=True)
    fig.suptitle(h5filename)

    n0 = abs(psi_fit)**2
    p0 = np.angle(psi_fit)

    kk = {'ticks': None, 'orientation': 'horizontal',
          'ticklocation': 'top'}  # read this from make_axes

    c1 = ax.imshow(n0, extent=extent)
    cax = ax.inset_axes([0, 1.06, 1, 0.04])
    plt.colorbar(c1, cax, **kk)

    c2 = ax_p.imshow(p0, cmap='RdBu', extent=extent)
    cax = ax_p.inset_axes([0, 1.06, 1, 0.04])
    plt.colorbar(c2, cax, **kk)

    R = abs(x.min())
    ax.set(xlim=(-R, R), ylim=(-R, R))
    ax_p.set(xlim=(-R, R), ylim=(-R, R))


    plt.show()


if __name__ == '__main__':
    plot_gs('build/groundstate_full.h5')
