# Create an object that ony
# holds data in several (possibly nested) fields.
# Adapted from Peter Norvig
# http://norvig.com/python-iaq.html

from items  import *
from rstring import *

class o:
  def __init__(i,**d)    : i.add(**d)
  def content(i)         : return i.__dict__
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k] 
  def __repr__(i)        : return rstring(i)
  def add(i,**d) :
    i.content().update(d)
    return i
  def blank(i):
    d = {key:None for key in i.content().keys()}
    return o(**d)
  def copy(i):
    return o(**i.content().copy())
    

