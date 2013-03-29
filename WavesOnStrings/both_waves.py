#!/usr/bin/env python
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# First set up the figure, the axis, and the plot element we want to animate
outerlim, innerlim = 4, 2
v1, v2 = 0.01, -0.01
fig = plt.figure()
ax = plt.axes(xlim=(-outerlim, outerlim), ylim=(-2, 2))
line1, = ax.plot([], [], lw=2, color='blue', alpha=0.5)
line2, = ax.plot([], [], lw=2, color='red', alpha=0.5)

# initialization function: plot the background of each frame
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2

# animation function.  This is called sequentially
x = np.linspace(-outerlim, outerlim, 2000)

def animate(t):
    y1 = np.sin(2 * np.pi * (x - v1 * t))
    y2 = np.sin(2 * np.pi * (x - v2 * t))
    line1.set_data(x, y1)
    line2.set_data(x, y2)
    return line1, line2

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=100, interval=20, blit=True)

plt.show()
