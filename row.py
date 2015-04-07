from lib import *

class Row:
  id=0
  def __init__(i,cells=[],t=None):
    Row.id = i.id = Row.id + 1
    i.cells = cells
    i.table = t 
    if t:
      for cell,value in zip(t.all,cells):
        if value is not the.TABLE.skip:
          cell += value
  def __getitem__(i,k): return i.cells[k]
  def __hash__(i)     : return i.id
  def __repr__(i): return '<'+str(i.cells)+'>'
  def far(i,z):
    mid = (i.lo + i.hi) * 0.5
    return i.hi if z < mid else i.lo
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