from lib import *

class Model:
  def __init__(i,fields=None):
    i.name = txt
  def ok(i,lst):
    return o(nums=[],syms=[])

def schaffer():
  def f1(x): return  x[0]**2
  def f2(x): return (x[0]-2)**2
  n=10**5
  o(x= [Num(lo= -1*n, hi=n)],
    y= [Num(name='f1'),
        Num(name='f2')])

def zdt4():
  n=10
  def f1(x): return x[0]
  def f2(x): return g(x)*(1- (x[0]/g(x))**2)
  def g(x) : return 1 + 10*(n - 1) + sum(
                h(x[i]) for i in range(1,n))
  def h(y):  return y**2 - 10*cos(4*pi*y)
     
   
