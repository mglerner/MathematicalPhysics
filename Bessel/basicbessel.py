#!/usr/bin/env python

from __future__ import division
from numpy import array, linspace
import scipy
import scipy.special
from scipy.special import j0,j1,jn,y0,y1,yn
import matplotlib.pyplot as pl

x = linspace(0,20,10000)

fig = pl.figure()

N = raw_input("How many bessel functions of the first kind to plot? ")
N = int(N)
for n in range(N):
    pl.plot(x,jn(n,x),label="$J_%s(x)$"%n)
pl.legend()
pl.grid('on')
pl.show()

N = raw_input("How many bessel functions of the second kind to plot? ")
pl.clf()
N = int(N)
for n in range(N):
    pl.plot(x,yn(n,x),label="$Y_%s(x)$"%n)
pl.legend()
pl.grid('on')
pl.show()

N = raw_input("Oops! How many bessel functions of the second kind to plot? ")
x0 = raw_input("Where to start x")
N,x0 = int(n),float(x0)
x = linspace(x0,20,10000)
pl.clf()
N = int(N)
for n in range(N):
    pl.plot(x,yn(n,x),label="$Y_%s(x)$"%n)
pl.legend()
pl.grid('on')
pl.show()

