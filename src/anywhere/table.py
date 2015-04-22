from lib import *

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
