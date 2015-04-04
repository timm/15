def has(x):
  if isinstance(x,(list,dict)):
    for y in x:
      for z in has(y):
        yield z
  else:
    yield x

def itemsAre(x):
  if "items" in dir(x):
    return {k:itemsAre(v) for k,v in x.items()}
  else:
    return d
