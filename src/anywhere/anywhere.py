from __future__ import print_function,division

from lib import *

  
#------------------------------------------------
def readcsv(file, t = None): 
  for cells in lines(file):
    if t:
      row(t,cells)
    else:
      t = table(cells)
  return t

def lines(file, bad  = r'(["\' \t\r\n]|#.*)',
                sep  = "" ) :
  def atom(x):
    try : return int(x)
    except ValueError:
      try : return float(x)
      except ValueError : return x
  kept = ""
  for line in open(file):
    now   = re.sub(bad,"",line)
    kept += now
    if kept:
      if not now[-1] == sep:
        yield map(atom, kept.split(sep))
        kept = ""
        
#------------------------------------------------    
def row(t,cells, skip='?'):
  t += [cells]
  for i,cell in enumerate(cells):
    if cell != skip:
      if i in t.num:
        hdr    = t.num[i]
        hdr.lo = min(cell, hdr.lo)
        hdr.hi = max(cell, hdr.hi)

def table(cells, num  = '$', less = '<',
                 more = '>', skip = "?" ):
  t = o(name={}, num={},  sym={},  rows=[],
        less={}, more={}, goal={},
        fields=cells )
  def nump(cell):
    for char in [num, less, more]:
      if char in cell:
         return True
  for i,cell in enumerate(cells):
    t.name[i] = cell
    if nump(cell):
      t.num[i] = o(hi = -1*10**32, lo = 10**32)
    else:
      t.sym[i] = i
    if less in cell:
      t.goal[i] = t.less[i] = i
    if more in cell:
      t.goal[i] = t.more[i] = i
    if not i in t.goal:
      t.indep[i] = i
  return t

def clone(t) { return table(t.fields) }
                    
#------------------------------------------------    
def norm(i,r):
  return (i - r.lo) / (r.hi - r.lo + 0.00001)

def trim(n,r):
  return max(r.lo, min(n, r.hi))

def dist(cells1,cells2,t, skip="?"):
  n = inc = 0
  for col in t.indep:
    x = cells1[col]
    y = cells2[col]
    if x==skip and y==skip:
      continue
    n += 1
    if col in t.sym:
      inc  += 0 if x==y else 1
    else:
      if x != skip: x= norm(x,t.num[col])
      if y != skip: y= norm(y,t.num[col])
      if x == skip: x= 1 if y<0.5 else 0
      if y == skip: y= 1 if x<0.5 else 0
      inc  += (x-y)**2
  return inc**0.5 / n**0.5

#------------------------------------------------    

