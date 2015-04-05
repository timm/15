# Create an object that ony
# holds data in several (possibly nested) fields.
# Adapted from Peter Norvig
# http://norvig.com/python-iaq.html

from items  import *
from string import *

class o:
  def __init__(i,**d)    : i.add(**d)
  def content(i)         : return i.__dict__
  def __setitem__(i,k,v) :  i.__dict__[k] = v
  def __repr__(i)        : return string(i)
  def add(i,**d) :
    i.content().update(d)
    return i
    

