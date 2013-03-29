#!/usr/bin/env python
from __future__ import division
import numpy as np
from numpy import linspace,cos
import matplotlib.pyplot as plt
from matplotlib import animation
import scipy
import scipy.special
from scipy.special import j0,j1,jn,k0,k1,kn,jn_zeros,kn_zeros

k10,k20,k30,k40,k50 = jn_zeros(0,5)
k11,k21,k31,k41,k51 = jn_zeros(1,5)

j = {0:j0,1:j1}
k = {
    1:{0:k10,1:k11},
    2:{0:k20,1:k21}
    }

# First set up the figure, the axis, and the plot element we want to animate
outerlim, innerlim = 4, 2
v = 1
fig = plt.figure()
ax = plt.axes(xlim=(-outerlim, outerlim), ylim=(-2, 2))
line, = ax.plot([], [], lw=2, color='red')

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
r = np.linspace(0, 1, 10000)

n = 0
m = 0
def animate(t):
    z = j[n](k[m][n]*r) * cos
    y = np.sin(2 * np.pi * (x - v * t))
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=100, interval=20, blit=True)

plt.show()
