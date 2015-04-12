from items import *
from rstring import *

class Emp:
  def __init__(i,who='tom'):
    i.name, i.shoeSize=who,23
  def  content(i): return "My name is %s" % i.name

class Point:
  def __init__(i,x=0,y=0):
    i.x,i.y=x,y
  def __repr__(i): return "(%s @ %s)" % (i.x,i.y)
  
def asdas(): return 1


lst= [Point(10,20),1,2,3,Emp('john'),asdas,[1],"asa",
                       [dict(a=4,
                            b=Emp('jane'),
                            c=[6,7,Point(20,100)]),
                       dict(d=[9,10],
                            e=10)]]

print contents(lst)

for y in items(lst):
  print y
  


print rstring([lst,[[[lst],lst],lst],[lst]])

