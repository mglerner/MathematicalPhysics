#!/usr/bin/env python

from __future__ import division
from numpy import array, linspace, zeros_like
import scipy
import scipy.special
from scipy.special import j0,j1,jn,y0,y1,yn
import matplotlib.pyplot as pl
from scipy.special import jn, jn_zeros

x = linspace(0,2,1000)

fig = pl.figure()

def k(m,n):
    # jn_zeros(n, nt): Compute nt zeros of the Bessel function Jn(x).
    return jn_zeros(n,m)[m-1] # m is 0-indexed here

def km0(m):
    #jn_zeros(n, nt): Compute nt zeros of the Bessel function Jn(x).
    # I.e. this returns an array, and we take the last element.
    return jn_zeros(0,m)[-1]



N = raw_input("How many bessel functions of the first kind to plot? ")
N = int(N)
y = zeros_like(x)
for m in range(1,N+1):
    km = km0(m)
    cm = 200/(km * jn(1,km))
    #print "cm",cm
    this_term = cm*jn(0,km*x)
    pl.plot(x,this_term,label="$Term %s$"%m)
    y = y + this_term
pl.plot(x,y,'k',linewidth=3,label='sum')
pl.legend()
pl.grid('on')
pl.show()
