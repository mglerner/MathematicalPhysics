#!/usr/bin/env python
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
outerlim, innerlim = 4, 2
v = -0.01
fig = plt.figure()
ax = plt.axes(xlim=(-outerlim, outerlim), ylim=(-2, 2))
line, = ax.plot([], [], lw=2, color='red')

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
x = np.linspace(-outerlim, outerlim, 2000)

def animate(t):
    y = np.sin(2 * np.pi * (x - v * t))
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=100, interval=20, blit=True)

plt.show()
