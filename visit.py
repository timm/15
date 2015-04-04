# things have  1) lists, 2) dicts, and
# 3) things that can report themselves as 
# things  and 4) other things

def has(x,
        filter=lambda z:z # process  each item
       ):
  "Return recursive contents, one at a time."
  if isinstance(x,(list,tuple)):
    for y in x:
      for z in has(y,filter):
        yield z
  elif isinstance(x,dict):
    for y in x.values():
      for z in has(y,filter):
        yield z
  elif 'has' in dir(x):
    for y in x.has():
      for z in has(y,filter):
        yield z
  else:
    yield filter(x)
    
def visit(x,
          filter=lambda z:z # process  each item
         ):
  "Return accumulated recursive contents."
  if isinstance(x,list):
    return [visit(y,filter) for y in x]
  elif isinstance(x,dict):
    return {k:visit(v,filter) for k,v in x.items()}
  elif 'has' in dir(x):
    return visit(x.has(),filter)
  else:
    return filter(x) 

def string(x):
  "Pretty print nested things." 
  import pprint # 
  def pretty(x):
    if x.__class__.__name__ == 'function':
      return x.__name__ + '()'
    else:
      return x  
  return pprint.pformat(visit(x,pretty))

