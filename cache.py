# cache.py

# For a tutorial on this code, 
# see second half of 101wrap.py

def cache(f):
  "Caching, simple case, no mirroring."
  name = f.__name__  
  def wrapper(i):
    if hasnot(i,"_cache"): i._cache = {}  
    key = (name, i.id)
    if key in i._cache:
      x = i._cache[key]
    else:
      x = f(i) # sigh, gonna have to call it
    i._cache[key] =  x # ensure ache holds 'c'
    return x
  return wrapper
  
def cache2(f):
  "Cache mirrored properties."
  name = f.__name__
  def wrapper(i,j):
    if hasnot(i,"_cache"): i._cache = {}  
    if hasnot(j,"_cache"): j._cache = {}
    if i.id > j.id: 
      i,j = j,i # ids now sorted Vv
    key = (name, i.id, j.id) 
    if key in i._cache:
      x = i._cache[key]
    elif key in j._cache:
      x = j._cache[key]
    else:
      x = f(i,j) # sigh, gonna have to call it
    i._cache[key] = j._cache[key] = x
    return x
  return wrapper