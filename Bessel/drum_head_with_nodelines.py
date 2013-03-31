#!/usr/bin/env python
from __future__ import print_function
"""
Based on the wireframe example script

If you make the plots, you can make the movie with

ffmpeg -q:a 5 -r 5 -b:v 19200 -i img%04d.png movie.mp4

or something similar.
"""
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

import numpy as np
from numpy import sin, cos, arctan, arctan2, array, sqrt, pi, linspace
import scipy
import scipy.special
from scipy.special import jn, jn_zeros
import time, sys, os

makeplots = True


v = 1
fns = 'cc'
ms = (1,2)
ms = (1,2,3)
ns = (0,1)
ns = (0,1,2)
    
f1 = {'s':sin,'c':cos}[fns[0]]
f2 = {'s':sin,'c':cos}[fns[1]]

def k(m,n):
    return jn_zeros(n,m)[m-1] # m is 0-indexed here


def generate(X, Y, t, m, n, v):
    theta = arctan2(Y,X)
    R = np.sqrt(X**2 + Y**2)
    # We know z = J_n(k*r)*      cos(n*theta)*cos(k*v*t)
    result =      jn(n,k(m,n)*R)*f1(n*theta)* f2(k(m,n)*v*t)
    result[R>1] = 0
    return result

plt.ion()
fig = plt.figure()
# It seems to me that things look best if you have 6 inches in width
# for each m and 2 in in height for each n.

fig.set_size_inches([6*len(ms),2*len(ns)])
axs = {}
rows, cols = len(ns), 2*len(ms)

idx = 1
for m in ms:
    axs[m] = {}
    for n in ns:
        axs[m][n] = (fig.add_subplot(rows,cols,idx, projection='3d'),
                    fig.add_subplot(rows,cols,idx+1))
        idx += 2
if 0:
    axs[1] = {0: (fig.add_subplot(rows,cols,1, projection='3d'), fig.add_subplot(rows,cols,2)),
              1: (fig.add_subplot(rows,cols,3, projection='3d'), fig.add_subplot(rows,cols,4)),}
    axs[2] = {0: (fig.add_subplot(rows,cols,5, projection='3d'), fig.add_subplot(rows,cols,6)),
              1: (fig.add_subplot(rows,cols,7, projection='3d'), fig.add_subplot(rows,cols,8)),}

xs = np.linspace(-1, 1, 100)
ys = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(xs, ys)
#Z = generate(X, Y, 0.0)

wframes = {}
contours = {}
for m in ms:
    wframes[m] = {}
    contours[m] = {}
    for n in ns:
        wframes[m][n] = None
        contours[m][n] = None

if makeplots:
    dname = fns[0]+fns[1] + '.'.join([str(i) for i in ms]) + '_' + '.'.join([str(i) for i in ns])
    if not os.path.exists(dname):
        os.makedirs(dname)
tstart = time.time()

first = True
frames_per = 50
periods = 2
# Note: unlike sin and cos, Jn's zeros are not integer multiples of
# each other.  Therefore, this loop goes over a defined number of
# periods of the lowest mode, but others won't fit evenly.
for (idx,t) in enumerate(np.linspace(0, periods*2*pi/jn_zeros(0,1)[0], periods*frames_per)):
    if not first:
        for m in ms:
            for n in ns:
                axs[m][n][0].collections.remove(wframes[m][n])
                for c in contours[m][n].collections:
                    axs[m][n][1].collections.remove(c)
                    
    first = False

    for m in ms:
        for n in ns:
            Z = generate(X, Y, t, m, n, v)
            wframes[m][n] = axs[m][n][0].plot_surface(X, Y, Z, rstride=4, cstride=4, alpha=0.3)

            if n == 0:
                axs[m][n][0].set_zlim(-0.7,.7)
                axs[m][n][1].imshow(Z,vmin=-0.7,vmax=0.7)
            else:
                axs[m][n][0].set_zlim(-0.5,0.5)
                axs[m][n][1].imshow(Z,vmin=-0.5,vmax=0.5)
            # The funny business with levels here is because you won't
            # get a contour exactly at zero that necessarily tracks
            # around both sides of the circle due to the fact that
            # we've discretized things.
            levels = [-0.000000001,0.0,0.000000001]
            contours[m][n] = axs[m][n][1].contour(Z, levels, colors='k',
                                                  linestyles='solid', linewidths=2)
    plt.draw()
    if makeplots:
        plt.savefig(dname + '/img' + '%04d'%(idx) + '.png')

print ('FPS: %f' % (periods*frames_per / (time.time() - tstart)))
