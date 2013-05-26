#!/usr/bin/env python3
# Written by Andres Erbsen and Sandra Schumann, distributed under the GNU GPLv3

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sys import argv

csvdata = (tuple(map(float,l.split())) for l in open(argv[1]).read().splitlines())

moved = []
painted = []
button_pressed = False
for (x,y,z,t,e) in csvdata:
    if e == 1:
        button_pressed = True
    elif e == 2:
        button_pressed = False
    if button_pressed:
        painted.append((x,y,z))
    else:
        moved.append((x,y,z))

ax = plt.figure().add_subplot(111, projection='3d')

ax.scatter(*zip(*moved[:1]), s=200, c='white', marker='H')
ax.scatter(*zip(*moved[1:]), c='white')
if painted: ax.scatter(*zip(*painted))

neg = min(map(min,moved+painted))
pos = max(map(max,moved+painted))
ax.auto_scale_xyz([neg, pos], [neg, pos], [neg, pos])
plt.show()

