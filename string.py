from items import *
import pprint

def string(x):
  "Pretty print nested content."   
  def pretty(x):
    if x.__class__.__name__ == 'function':
      return x.__name__ + '()'
    elif isinstance(x,float):
      return '%g' % x
    else:
      return x  
  return pprint.pformat(contents(x,pretty))
