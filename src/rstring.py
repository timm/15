from items import *
import pprint

def rstring(x):
  "Pretty print nested content."
  def skip(x):
    return str(x)[0] == "_"
  def pretty(x):
    if x.__class__.__name__ == 'function':
      return x.__name__ + '()'
    elif isinstance(x,float):
      return '%g' % x
    else:
      return x  
  return pprint.pformat(contents(x,pretty,skip),
                        indent=2, width=60)
