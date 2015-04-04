from __future__ import print_function
from has import *

class Emp:
  def __init__(i):
    i.name, i.shoeSize='tim',23
  def  items(i): return i.__dict__

def asdas(): return 1

lst= [1,2,3,Emp(),asdas,[1],
                       [dict(a=4,
                            b=5,
                            c=[6,7,8]),
                       dict(d=[9,10],
                            e=10)]]
print([x for x in has(lst)])

print([x for x in  has(Emp())])

print(round.__class__)



