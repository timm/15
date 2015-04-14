from __future__ import division
import math

e    = math.e
pi   = math.pi
log  = math.log
sin  = math.sin
cos  = math.cos
sqrt = math.sqrt

def normpdf(mean, sd, x):
  var   = sd**2
  denom = sqrt(2*pi*var)
  num   = math.exp(-(x-mean)**2/(2*var))
  return num/denom

def nearly(x,y,p=0.001):
  return abs(x-y)/x < p

def ntiles(lst, tiles=[0.1,0.3,0.5,0.7,0.9]):
  at = lambda x: lst[ int(len(lst)*x) ]
  return [ at(tile) for tile in tiles ]

def gs(lst):
  return map(lambda x: round(x,5), lst)
