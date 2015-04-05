# things contain 1) lists or 2) dicts or
# 3) things that can report themselves as 
# things  and 4) other things

def contents(x, filter=lambda z:z):
  "Recursively accumulate contents."
  if isinstance(x,list):
    return [contents(y,filter) for y in x]
  elif isinstance(x,dict):
    return {k:contents(v,filter) for k,v in x.items()}
  elif 'content' in dir(x):
    return contents(x.content(),filter)
#  elif hasattr(x,"__dict__"):
#     return contents({x.__class__.__name__:
#                      x.__dict__})
  else:
    return filter(x) 

def items(x, filter=lambda z:z):
  "Recursively return contents."
  def iterate(x) :
    if   isinstance(x,(list,tuple)): return x
    elif isinstance(x,dict)        : return x.values()
    elif 'content' in dir(x)       : return x.content()
  it = iterate(x)
  if it:
    for y in it:
      for z in items(y,filter):
        yield z
  else:
    yield filter(x)
