
def quartile(lst,min=0,max=100,width=50,
             chops=[0.1 ,0.3,0.5,0.7,0.9],
             marks=["-" ," "," ","-"," "],
             on="-", off=" ",bar="|",format=" %3.0f"):
  def pos(p)   : return ordered[int(len(lst)*p)]
  def place(x) : return int(width*float((x - min))/(max - min))
  def pairs(lst):
      last=lst[0]
      for i in lst[1:]:
        yield last,i
        last = i
  def pretty(lst) : 
      return ' '+(', '.join([format % x for x in lst]))+ ' '
  ordered = sorted(lst)
  what  = [pos(p) for p in chops]
  where = [place(n) for n in  what]
  out   = [" "] * width
  for one,two in pairs(where):
    for i in range(one,two): 
       out[i] = marks[0]
    marks = marks[1:]
  out[width/2] = bar
  out[place(pos(0.5))] = "*" 
  return ''.join(out) +  "," +  pretty(what)
