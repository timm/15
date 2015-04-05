from __future__ import print_function,division
from o import *

x= o(name= 'tom',
     weight=o(aa=20,bb=3)
    ).add(name='tim',height=20)

x.weight.aa = 30

print(x)
print(x.weight.bb)
