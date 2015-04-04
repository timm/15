from has import *

class o:
  def __init__(i,**d) : i.add(**d)
  def __iadd__(i,**d) : i.has().update(**d); return i
  def has(i)          : i.__dict__
  def __repr__(i)     : return string(i.has())
    

o(name=21,
        wiehgt=o(aa=2,bb=3)))
      
