(setting,obs)

setting = (dec,conf)

def eval(dec): objs

create 30 centers

class magic:
  def has(i,**d): i.__dict__.update(d); return i

class setting:
    def __init__(i,dec,conf,f):
      i.has(dec=dec,conf=conf,f=f,n=1)
    def obj(i,dec=None):
      return i.f(dec or i.dec)
    def eat(i,(dec,conf)):
      us  = i.obj(i.dec)
		  them= i.obj(dec) 
