class Bag:
  def __init__(i,rx,lst=[]) :  # intialization
    i.sq = i.sum = i.n = 0.0; i.rx = rx; i.rank = 0
    i.all=[]; i._median=None
    for x in lst: i.keep(x)
  def keep(i,x) : # using 'x', increment some counters 
    i._median=None
    i.all.append(x); i.n += 1 ; i.sum += x; i.sq += x*x
  def median(i):
    if not i._median: 
       i.all   = sorted(i.all)
       i._median = i.all[ int(len(i.all)/2) ]
    return i._median
  def mu(i) :  # mean
    return i.sum / i.n
  def stdev(i): # standard deviation
    return ((i.sq-((i.sum*i.sum)/i.n))/(i.n-1))**0.5
  def __repr__(i) :
    return '"' + str(i.rx) + '" : ' +str(i.all) + \
           ' mean = ' + str(i.mu())+   " rank = #"+str(i.rank)
  def __lt__(i,j): # implement bag1 < bag2
    return i.median()<  j.median()
  def __add__(i,j): # implement bag1 + bag2
    k=Bag("+")
    k.n=i.n+j.n; k.sum=i.sum+j.sum; k.sq=i.sq+j.sq 
    return k 
  def __sub__(i,j) : # implement bag1 - bag2
    k=Bag("-")
    k.n=i.n-j.n; k.sum=i.sum-j.sum; k.sq=i.sq-j.sq
    return k
