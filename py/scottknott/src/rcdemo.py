from rfun import *
from bag  import Bag

print "Demo1: finds three ranks"

rc([Bag("x1",[0.34, 0.49, 0.51, 0.6]),
    Bag("x2",[0.6,  0.7,  0.8,  0.9]),
    Bag("x3",[0.15, 0.25, 0.4,  0.35]),
    Bag("x4",[0.6,  0.7,  0.8,  0.9]),
    Bag("x5",[0.1,  0.2,  0.3,  0.4]) ])

print "\nDemo2: finds one rank (a.k.a. blurring)";

rc([Bag("y1",[101, 100, 99,   101,  99.5]), 
    Bag("y2",[101, 100, 99,   101, 100]),
    Bag("y3",[101, 100, 99.5, 101,  99]),
    Bag("y4",[101, 100, 99,   101, 100]) ])
