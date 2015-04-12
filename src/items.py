# things contain 1) lists or 2) dicts or
# 3) things that can report themselves as 
# things  and 4) other things

def contents(x,
             filter=lambda z:z,
             skip  =lambda z: False):
  "Recursively accumulate contents."
  if isinstance(x,list):
    return [contents(y,filter,skip) for y in x]
  elif isinstance(x,dict):
    return {k:contents(v,filter,skip)
            for k,v in x.items() if not skip(k)}
  elif 'content' in dir(x):
    return contents(x.content(),filter,skip)
#  elif hasattr(x,"__dict__"):
#     return contents({x.__class__.__name__:
#                      x.__dict__})
  else:
    return filter(x) 

def items(x, filter=lambda z:z):
  "Recursively return contents."
  def isa(x,y): return isinstance(x,y)
  def iterate(x) :
    if   isa(x,(list,tuple)): return x
    elif isa(x,dict)        : return x.values()
    elif 'content' in dir(x): return x.content()
  it = iterate(x)
  if it:
    for y in it:
      for z in items(y,filter):
        yield z
  else:
    yield filter(x)
