class Bag:
  def __init__(i,rx,lst=[]) :  # intialization
    i.n = 0; i.mean = 0.0; i.m2 = 0.0
    i.rx = rx; i.rank = 0
    for x in lst: i.keep(x)

  def keep(i,x) : # using 'x', increment some counters 
    i.n    += 1 ; delta = x - i.mean;
    i.mean += delta/i.n
    i.m2   += delta * (x - i.mean)

  def mu(i) :  # mean
    return i.sum / i.n

  def stdev(i): # standard deviation
    return (i.m2 / (i.n - 1))**0.5

  def __repr__(i) :
    return "ranked #"+str(i.rank)+' is '+ \
           str(i.rx) + ' with ' + str(i.mu())

  def __lt__(i,j): # implement bag1 < bag2
    return i.mu()<  j.mu()

  def __add__(i,j): # implement bag1 + bag2
    k=Bag("+")
    k.n=i.n+j.n; k.sum=i.sum+j.sum; k.sq=i.sq+j.sq 
    return k 

  def __sub__(i,j) : # implement bag1 - bag2
    k=Bag("-")
    k.n=i.n-j.n; k.sum=i.sum-j.sum; k.sq=i.sq-j.sq
    return k

b= Bag("stuff",[1,2,3,4,5,10])

print b.stdev()

def online_variance(data):
    n = 0
    mean = 0.0
    M2 = 0.0
    for x in data:
        n    = n + 1
        delta = x - mean
        mean  = mean + delta/n
        M2    = M2 + delta*(x - mean)
    variance_n = M2/n
    variance   = M2/(n - 1)
    return (variance**0.5, variance_n**0.5)

print online_variance([1,2,3,4,5,10])
