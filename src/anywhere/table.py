from lib import *

@settings
def TBL(): return o(
    bad  = r'(["\' \t\r\n]|#.*)',
    sep  = ",",
    skip = "?",
    num  = '$',
    less = '<',
    more = '>'
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
  t = o(num={},  sym={},  rows=[], all =[],
        less={}, more={}, goal={}, fields=cells)
  my=the.TBL
  def nump(cell):
    for char in [my.num, my.less, my.more]:
      if char in cell:
         return True
  for i,cell in enumerate(cells):
    if nump(cell):
      hdr = t.num[i] = Num()  
    else:
      hdr = t.sym[i] = Sym()
    hdr.txt  = cell
    hdr.pos  = i
    i.all += [hdr]
    if my.less in cell: t.goal[i] = t.less[i] = hdr
    if my.more in cell: t.goal[i] = t.more[i] = hdr
    if not i in t.goal: t.indep[i]= hdr
    i.all += [hdr]
  return t

def clone(t) { return table0(t.fields) }

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
        tmp = cell[hdr.i]
        if tmp != the.TBL.skip:
           hdr += cell[hdr.i]
  def __getitem__(i,k): return i.cells[k]
  def __hash__(i)     : return i.id
  def __repr__(i): return '<'+str(i.cells)+'>'

  
  #@memo2
  def dist(i,j):
    n = all = 0
    for v1,v2,hdr in cells2(i,j,i.table.indep):
      v1   = hdr.norm(v1)
      v2   = hdr.norm(v2)
      n   += 1
      all += hdr.dist(v1,v2) 
    return all**0.5 / (n+0.000001)**0.5
    
def cells2(row1,row2,headers):
  skip = lambda z: z == the.TABLE.skip
  for header in headers:
    v1 = row1[header.col]
    v2 = row2[header.col]
    if not (skip(v1) and skip(v2)):
      if skip(v1): v1 = hdr.far(v2)
      if skip(v2): v2 = hdr.far(v1)
      yield v1, v2, header
