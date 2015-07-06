"""
Actory: a Python-based domain-specific language (DSL) for 
specifying finite state machines (FSM).

In these machines, actions change state.

Copyright 2012, Tim Menzies, 
Creative Commons Attribution 3.0 Unported License.
Share and enjoy. 
:-)

"""

from pprint import pprint
from contextlib import contextmanager
import random
any=random.choice
r= random.random

class o:
  ids = {}
  latest = {}
  def __init__(i,**d):
    k = i.__class__.__name__
    i.id = o.ids[k] = o.ids.get(k) + 1
    i.has().update(d)
    o.latest[k] = i
  def has(i):
    return i.__dict__
  def __repr__(i):
    return str(i.__class__.__name__ + str(i.has()))
  
class State(o):
  def __init__(i,name='',terminal=False):
    i.name,i.terminal = name,terminal
    i.machine = o.latest('Machine')
  def onEntry(i,w)  : i.say('Entering')
  def onExit(i,w)   : i.say('Exiting')
  def onStay(i,w)   : pass
	def say(i,txt)    : print txt+">> "+i.name
    
def Trans(o):
  def __init__(i,here=None,there=None,tag='',
               gaurd=lambda z: True):
    i.here, i.there,i.tag=here,there,tag
    i.gaurd = i.gaurd
    o.latest['Machine'].trans += [i]
  def ready(i):
    return i.guard()

def run(machine,steps=1000,w=o()):
  while True:
    for tran in any(machine.trans):
      if tran.ready() :
        tran.here.onExit(w)
				tran.there.onEntry(w)
      else:
        tran.here.onStay(w)
			machine = tran.here.machine
      steps -= 1
      if steps < 1 or here.terminal:
        return
      
class Machine(o):
	def __init__(i,str=None,trans=[]) :
		i.trans = trans
    i.name  = str or 'M'+str(i.id)

S,T,M  = State,Trans,Machine
_S = lambda tag: S(tag,terminal=True)

@contextmanager
def machine(txt):
  m = Machine(txt)
  yield m
  yield m

def chess():
  with machine('chess') as m:
    w    =  S('whitesTurn')
	  b    =  S('blacksTurn')
	  bwin = _S('blackWins')
	  draw = _S('draw')
	  wwin = _S('whiteWins')
    T(w,b,   'white moves')
    T(b,w,   'black moves')
    T(w,bwin,'checkmate')
    T(w,draw,'stalemate')
	  T(b,draw,'stalemate')
    T(b,wwin,'checkmate')
  return m

