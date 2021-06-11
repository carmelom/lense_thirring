#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Created: 07-2020 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

_x = np.linspace(-10, 10, 256)
X, Y = np.meshgrid(_x, _x)

X = X - X.mean()
Y = Y - Y.mean()

x0 = 10

# phase = np.arctan2(Y, (X - x0))
radius = 7
nu = 1
xv = 3
dv = 0.7


phase = nu * np.arctan2(Y, X)
phase += np.arctan2(Y, X - xv + dv) + np.arctan2(-Y, X - xv - dv)

plt.imshow(phase, cmap='RdBu', extent=(X.min(), X.max(), Y.min(), Y.max()))
plt.gca().add_patch(Circle((0, 0), radius, ec='k', fc='none'))
plt.colorbar()
plt.show()
