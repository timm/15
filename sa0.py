class o:
  def __init__(i,**d)    : i.__dict__.update(d)
  def __setitem__(i,k,v) : i.__dict__[k] = v
  def __getitem__(i,k)   : return i.__dict__[k]
  def __repr__(i)        : return 'o'+str(i.__dict__)

def lt(x,y): return x < y
def gt(x,y): return x > y

class Less:
    def __init__(txt,make=fun,better=lt):
        i.better = better
        i.txt,i.make = txt,make
    def __call__():
        return i.make()

def More(*l,**d): return Less(*l,**d,better=gt)

class ZDT1(Candidate):
  n=30
  def about(i):
    def f1(can):
      return can.decs[0]
    def f2(can):
      g = 1 + 9*sum(x for x in can.decs[1:] )/(ZDT1.n-1)
      return g*abs(1 - sqrt(can.decs[0]*g))
    def dec(x):
      return An(x,lo=0,hi=1)
    i.decs = [dec(x) for x in range(ZDT1.n)]
    i.objs = [Less("f1",maker=f1),
              Less("f2",maker=f2)]
