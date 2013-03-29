#!/usr/bin/env python
from __future__ import division
import numpy as np
from numpy import sin, cos, pi, linspace, zeros, zeros_like, ones, ones_like, arange
import matplotlib.pyplot as plt
from matplotlib import animation

N = raw_input("Number of terms: ")
N = int(N)

# First set up the figure, the axis, and the plot element we want to animate
l, h, w = 1.0, 0.04, 0.06
v = 0.01
fig = plt.figure()
ax = plt.axes(xlim=(0, l), ylim=(-1.2*h, 1.2*h))
plt.grid('on')
plt.xticks(arange(0,l,w/2))
line, = ax.plot([], [], lw=2, color='red')

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
x = linspace(0, l, 2000)

def animate(t):
    y = zeros_like(x)
    for n in range(1,N+1,2): # range starts at zero
        pre = (-1)**((n-1)/2)
        y = y +  pre * (1/n**2) * (sin(n*pi*w/l)*sin(n*pi*x/l)*sin(n*pi*v*t/l))


    #y = ( (4*h*l)/(pi*pi*v) ) * y
    y = ( (4*h*l)/(pi*pi*w) ) * y

    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

plt.show()
