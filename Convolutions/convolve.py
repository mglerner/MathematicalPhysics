#!/usr/bin/env python
"""
We'll define our functions from -pi to pi, and we'll plot from -3pi to 3pi
u1 moves, u2 doesn't in our convention
"""
from __future__ import division
import numpy as np
from numpy import pi, linspace, ones_like, arange, sin, cos, zeros_like, abs
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()
nx = 1000
fullx = linspace(-3*pi, 3*pi, 3*nx+1)        # x-array
subx = linspace(-pi, pi, nx+1)
dx = subx[1]-subx[0]
Shapes = {}

Shapes['bigbox'] = ones_like(subx)
Shapes['sin'] = sin(subx)
Shapes['sin(2x)'] = sin(2*subx)
Shapes['sin(5x)'] = sin(5*subx)
Shapes['smallbox'] = zeros_like(subx)
Shapes['smallbox'][int(Shapes['smallbox'].shape[0]/4):int(Shapes['smallbox'].shape[0]*3/4)] = 1.
Shapes['x2'] = subx**2
Shapes['smallx2'] = subx**2
Shapes['smallx2'][0:int(Shapes['smallbox'].shape[0]/4)] = 0.
Shapes['smallx2'][int(Shapes['smallbox'].shape[0]*3/4):] = 0.
Shapes['x'] = subx
Shapes['negwedge'] = Shapes['x'].copy()
Shapes['negwedge'][0:subx.shape[0]] += Shapes['negwedge'][0]

Shapes['poswedge'] = Shapes['x'].copy()
Shapes['poswedge'][0:subx.shape[0]] -= Shapes['poswedge'][0]


Shapes['smallwedge'] = zeros_like(subx)
Shapes['smallwedge'][0:int(subx.shape[0])/2] = Shapes['poswedge'][0:int(subx.shape[0])/2]

Shapes['saw'] = Shapes['smallwedge'].copy()
Shapes['saw'][int(subx.shape[0])/2:] = Shapes['negwedge'][int(subx.shape[0])/2:]

Shapes['triangle'] = Shapes['saw'].copy()
Shapes['triangle'][int(subx.shape[0])/2:] = -Shapes['saw'][int(subx.shape[0])/2:]
u1 = 'x'
u2 ='sin(5x)'

_u1 = Shapes[u1]
_u2 = Shapes[u2]
yconv = zeros_like(fullx)
line1, = ax.plot(fullx, yconv, label=u1)
line2, = ax.plot(fullx, yconv, label=u2)
line3, = ax.plot(fullx, yconv,'k--',linewidth=2,label=u1+r' $\ast$ ' + u2)
#overlap = ax.fill_between(fullx, _u1, _u2, color='y',alpha=.3)
dy1 = abs(_u1).sum()*dx
dy2 = abs(_u2).sum()*dx
dy = dy1*dy2/5
print dy1, dy2, dy
ax.set_ylim([-1.1*dy,1.1*dy])
ax.legend()

def animate(i):
    y1 = zeros_like(fullx)
    y2 = zeros_like(fullx)
    y1[i:i+subx.shape[0]] = _u1
    y2[subx.shape[0]:2*subx.shape[0]] = _u2
    _yconv = (y1 * y2 * dx).sum()
    yconv[int(subx.shape[0]/2)+i] = _yconv
    if i == 0:
        for j in range(yconv.shape[0]):
            yconv[j] = 0


    line1.set_ydata(y1)  # update the data
    line2.set_ydata(y2)  # update the data
    line3.set_ydata(yconv)  # update the data
    overlap = ax.fill_between(fullx, y1, y2, color='k',alpha=.3)
    ax.legend()
    return line1,line2,line3

#Init only required for blitting to give a clean slate.
def init():
    line1.set_ydata(np.ma.array(zeros_like(fullx), mask=True))
    line2.set_ydata(np.ma.array(zeros_like(fullx), mask=True))
    line3.set_ydata(np.ma.array(zeros_like(fullx), mask=True))
    return line1,line2,line3

ani = animation.FuncAnimation(fig, animate, fullx.shape[0] - subx.shape[0], init_func=init,
                              interval=2, blit=True, repeat_delay = 500, repeat = True)
plt.show()
