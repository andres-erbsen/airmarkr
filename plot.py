#!/usr/bin/env python3
# Written by Andres Erbsen and Sandra Schumann, distributed under the GNU GPLv3

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sys import argv

toklines = [l.split(',')[:3] for l in open(argv[1]).read().splitlines()]
coords = [(float(x), float(y), float(z)) for (x,y,z) in toklines ]
x0,y0,z0 = list(zip(*coords[:1]))
xs,ys,zs = list(zip(*coords))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(xs, ys, zs)
ax.scatter(x0, y0, z0, s=200, c='white', marker='H')


neg, pos = min([min(xs),min(ys),min(zs)]), max([max(xs),max(ys),max(zs)])
ax.auto_scale_xyz([neg, pos], [neg, pos], [neg, pos])
plt.show()
