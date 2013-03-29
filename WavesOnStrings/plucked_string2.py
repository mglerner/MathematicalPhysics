#!/usr/bin/env python
from __future__ import division
import numpy as np
from numpy import sin, cos, pi, linspace
import matplotlib.pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
l,h = 1.0, 0.4
v = 0.01
fig = plt.figure()
ax = plt.axes(xlim=(0, l), ylim=(-1.2*h, 1.2*h))
line, = ax.plot([], [], lw=2, color='red')

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
x = linspace(0, l, 2000)

def animate(t):
    y = ((8*h)/(pi*pi)) * (sin(pi*x/l)*cos(pi*v*t/l) - (1/9)*sin(3*pi*x/l)*cos(3*pi*v*t/l) )
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

plt.show()
