from __future__ import division
import math

pi   = math.pi
log  = math.log
sqrt = math.sqrt
cos  = math.cos

def normpdf(mean, sd, x):
  var   = sd**2
  denom = sqrt(2*pi*var)
  num   = math.exp(-(x-mean)**2/(2*var))
  return num/denom

def nearly(x,y,p=0.001):
  return abs(x-y)/x < p
