#!/usr/bin/env python
from __future__ import division
import numpy as np
from numpy import *
import matplotlib
#matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from scipy.special import jn, jn_zeros

def k(m,n):
    return jn_zeros(n,m)[m-1] # m is 0-indexed here

xs = linspace(-1, 1, 100)
ys = linspace(-1, 1, 100)
X, Y = meshgrid(xs, ys)
fns = 'cc'
f1 = {'s':sin,'c':cos}[fns[0]]
f2 = {'s':sin,'c':cos}[fns[1]]
n, m = 1, 1
v = 1
NT = 400
dt = 10/NT

def getZ(X, Y, i):
    global m,n,f1,f2,dt
    t = i * dt
    theta = arctan2(Y,X) # This does arctan(Y/X) but gets the sign right.
    R = sqrt(X**2 + Y**2)
    # We know z = J_n(k*r)*cos(n*theta)*cos(k*v*t)
    # 
    result = jn(n,k(m,n)*R)*f1(n*theta)*f2(k(m,n)*v*t)
    result[R>1] = 0  # we plot points from the square, but physically require this.
    return result


fig = plt.figure()
ax = plt.gca(projection='3d')#Axes3D(fig)
#wireframe = ax.plot_surface(X, Y, getZ(X,Y,0.0), rstride=2, cstride=2,cmap=cm.jet)
wireframe = ax.plot_surface(X, Y, getZ(X,Y,0.0), rstride=4, cstride=4, cmap=cm.jet, alpha=0.3)

ax.set_zlim(-1,1)
ax.axis("off")
ax.set_frame_on(False)

# precalculate Z

Z = [getZ(X,Y,i) for i in range(NT)]

def animate(i, ax, fig):
    global X,Y,Z
    global m,n
    #Z = getZ(X,Y,i)
    ax.cla()
    wireframe = ax.plot_surface(X, Y, Z[i], rstride=4, cstride=4, cmap=cm.jet, alpha=0.3)
    if n == 0:
        ax.set_zlim(-1,1)
    else:
        ax.set_zlim(-0.5,0.5)
    # ax = plt.gca(projection='3d'); ax._axis3don = False
    ax.axis("off")
    ax.set_frame_on(False)
    # frame.axes.get_xaxis().set_visible(False)
    # frame.axes.get_yaxis().set_visible(False)
    # ax.set_frame_on(False)
    #ax.view_init(elev=25., azim=140)
    return wireframe,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, frames=NT, fargs=(ax, fig), interval=2)
 
# this is how you save your animation to file:
#anim.save('2d_sor_unstable.gif', writer='imagemagick', fps=30)
 
plt.show()
