from __future__ import division,print_function
import sys
sys.dont_write_bytecode = True

def go(f):
  print(f.__name__)
  f()
