import sys,random,math
sys.dont_write_bytecode=True

def reallyLessThan(y0,z0,conf=0.05,b=100):
  class Sum():
    def __init__(i,some=[]):
      i.sum = i.n = i.mu = 0 ; i.all=[]
      for one in some: i.put(one)
    def put(i,x):
      i.all.append(x);
      i.sum +=x; i.n += 1; i.mu = float(i.sum)/i.n
    def __add__(i1,i2): return Sum(i1.all + i2.all)
  def testStatistic(y,z): 
     tmp1 = tmp2 = 0
     for y1 in y.all: tmp1 += (y1 - y.mu)**2 
     for z1 in z.all: tmp2 += (z1 - z.mu)**2
     s1    = float(tmp1)/(y.n - 1)
     s2    = float(tmp2)/(z.n - 1)
     delta = z.mu - y.mu
     if s1+s2:
       delta =  delta/((s1/y.n + s2/z.n)**0.5)
     return delta
  def one(lst): return lst[ int(any(len(lst))) ]
  def any(n)  : return random.uniform(0,n)
  y,z  = Sum(y0), Sum(z0)
  x    = y + z
  tobs = testStatistic(y,z)
  yhat = [y1 - y.mu + x.mu for y1 in y.all]
  zhat = [z1 - z.mu + x.mu for z1 in z.all]
  bigger = 0.0
  for i in range(b):
    if testStatistic(Sum([one(yhat) for _ in yhat]),
                     Sum([one(zhat) for _ in zhat])) > tobs:
      bigger += 1
  return bigger / b < conf

def test(n=30,mu1=10,sigma1=1,mu2=10.2,sigma2=1):
   def g(mu,sigma) : return random.gauss(mu,sigma)
   x = [g(mu1,sigma1) for i in range(n)]
   y = [g(mu2,sigma2) for i in range(n)]
   return n,mu1,sigma1,mu2,sigma2,\
          'different' if reallyLessThan(x,y) else 'same'

print   test(30, 10.1, 1, 10.2, 1)
print   test(30, 10.1, 1, 10.8, 1)
print   test(30, 10.1, 10, 10.8, 1)

