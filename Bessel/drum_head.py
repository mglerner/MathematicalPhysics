#!/usr/bin/env python
from __future__ import division
"""
Based on the wireframe example script
"""
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
from numpy import sin, cos, arctan, arctan2, array, sqrt, linspace, meshgrid
import scipy
import scipy.special
from scipy.special import jn, jn_zeros
import time, sys, os

v = 1
n, m = 1, 1
if len(sys.argv) >= 3:
    n,m = [int(i) for i in sys.argv[1:3]]
if m == 0:
    sys.exit("M must be greater than or equal to 1")

if len(sys.argv) >= 4:
    fns = sys.argv[3]
else:
    fns = 'cc'
    
f1 = {'s':sin,'c':cos}[fns[0]]
f2 = {'s':sin,'c':cos}[fns[1]]

def k(m,n):
    return jn_zeros(n,m)[m-1] # m is 0-indexed here

def generate(X, Y, t):
    theta = arctan2(Y,X) # This does arctan(Y/X) but gets the sign right.
    R = sqrt(X**2 + Y**2)
    # We know z = J_n(k*r)*cos(n*theta)*cos(k*v*t)
    # 
    result = jn(n,k(m,n)*R)*f1(n*theta)*f2(k(m,n)*v*t)
    result[R>1] = 0  # we plot points from the square, but physically require this.
    return result

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs = linspace(-1, 1, 100)
ys = linspace(-1, 1, 100)
X, Y = meshgrid(xs, ys)
Z = generate(X, Y, 0.0)

wframe = None
tstart = time.time()
for t in linspace(0, 10, 400):
    oldcol = wframe
    Z = generate(X, Y, t)
    #wframe = ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2)
    wframe = ax.plot_surface(X, Y, Z, rstride=4, cstride=4, alpha=0.3)

    # Remove old line collection before drawing
    if oldcol is not None:
        ax.collections.remove(oldcol)
    if n == 0:
        ax.set_zlim(-1,1)
    else:
        ax.set_zlim(-0.5,0.5)
    plt.draw()
