#!/usr/bin/env python
from __future__ import print_function
"""
Based on the wireframe example script
"""
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np
from numpy import sin, cos, arctan, arctan2, array, sqrt
import scipy
import scipy.special
from scipy.special import jn, jn_zeros
import time, sys, os

v = 1
n = 1
m = 1
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
    #R = 1 - sqrt(X**2 + Y**2)
    #theta = arctan(Y/X)
    theta = arctan2(Y,X)
    R = np.sqrt(X**2 + Y**2)
    # We know z = J_n(k*r)*cos(n*theta)*cos(k*v*t)
    # 
    result = jn(n,k(m,n)*R)*f1(n*theta)*f2(k(m,n)*v*t)
    result[R>1] = 0
    return result

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


xs = np.linspace(-1, 1, 100)
ys = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(xs, ys)
Z = generate(X, Y, 0.0)

wframe = None

dname = '%sk%s%s'%(fns,m,n)
os.makedirs(dname)
tstart = time.time()
for t in np.linspace(0, 10, 400):

    oldcol = wframe
    #oldcs1 = cs1

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
    plt.savefig(dname + '/img' + '%04d'%(t*400) + '.png')

print ('FPS: %f' % (100 / (time.time() - tstart)))
