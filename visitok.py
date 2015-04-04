from visit import *

class Emp:
  def __init__(i):
    i.name, i.shoeSize='tim',23
  def  has(i): return "EMP=",i.__dict__

def asdas(): return 1

print "has" in dir(Emp())

lst= [1,2,3,Emp(),asdas,[1],
                       [dict(a=4,
                            b=Emp(),
                            c=[6,7,Emp()]),
                       dict(d=[9,10],
                            e=10)]]

for y in has(lst):
  print y
  
print string([lst,[[[lst],lst],lst],[lst]])



