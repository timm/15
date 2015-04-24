from lib import *
from col import *

@setting
def TBL(): return o(
    bad  = r'(["\' \t\r\n]|#.*)',
    sep  = ",",
    skip = "?",
    num  = '$',
    less = '<',
    more = '>',
    norm = True
)

def readcsv(file, t = None): 
  for cells in lines(file):
    if t:
      Row(cells,t)
    else:
      t = table0(cells)
  return t

def lines(file) :
  def atom(x):
    try : return int(x)
    except ValueError:
      try : return float(x)
      except ValueError : return x
  kept = ""
  for line in open(file):
    now   = re.sub(the.TBL.bad,"",line)
    kept += now
    if kept:
      if not now[-1] == the.TBL.sep:
        yield map(atom, kept.split(the.TBL.sep))
        kept = ""

def table0(cells):
  t = o(num={},  sym={},  rows=[], all =[],indep={},
        less={}, more={}, goal={}, fields=cells)
  my= the.TBL
  def nump(cell):
    for char in [my.num, my.less, my.more]:
      if char in cell:
        return True
  for i,cell in enumerate(cells):
    if nump(cell):
      hdr = t.num[i] = Num()  
    else:
      hdr = t.sym[i] = Sym()
    hdr.txt = cell
    hdr.pos = i
    t.all += [hdr]
    if my.less in cell: t.goal[i] = t.less[i] = hdr
    if my.more in cell: t.goal[i] = t.more[i] = hdr
    if not i in t.goal: t.indep[i]= hdr
  return t

def clone(t): return table0(t.fields) 

class Row:
  id=0
  def __init__(i,cells=[],t=None):
    Row.id  = i.id = Row.id + 1
    i.cells = cells
    i.cache = None
    if t:
      i.table = t
      t.rows += [cells]
      for hdr in t.all:
        tmp = cells[hdr.pos]
        if tmp != the.TBL.skip:
          hdr += tmp
  def __getitem__(i,k): return i.cells[k]
  def __sub__(i,j)    : return dist(i,j,i.table)
  def __hash__(i)     : return i.id
  def __repr__(i)     : return '<'+str(i.cells)+'>'
  @cache
  def fromHell(i) :
    def from1(hdr, x, hell):
      x = hdr.norm(x) if the.TBL.norm else x
      return (x - hell)**2 
    n = inc = 0
    for hdr in t.more.values():
      n   += 1
      inc += from1(hdr, i[hdr.pos], 
                   0 if the.TBL.norm else hdr.lo)
    for hdr in t.less.values():
      n   += 1
      inc += from1(hdr, i[hdr.pos], 
                   1 if the.TBL.norm else hdr.lo)
    return inc**0.5 / n**0.5    

def dist(i,j,t):
  n = inc = 0
  skip = the.TBL.skip
  for hdr in t.indep.values():
    k    = hdr.pos
    x, y = i[k], j[k]
    if x == y == skip:
      continue
    n += 1
    if k in t.sym:
      inc += 0 if x==y else 1
    else:
      lo, hi = hdr.lo, hdr.hi
      mid    = (hdr.hi - hdr.lo)/2
      if the.TBL.norm:
        if x != skip: x = hdr.norm(x)
        if y != skip: y = hdr.norm(y)
        lo, hi, mid = 0, 1, 0.5
      if x == skip: x = hi if y < mid else lo
      if y == skip: y = hi if x < mid else lo
      inc += (x-y)**2
  return inc**0.5 / (n + 0.000001)**0.5
