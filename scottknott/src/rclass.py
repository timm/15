class R:
  def now0(self) : 
    "initialize a result counter"
    return -1
  def better(self,old,new) : 
    "check if a new counter is better than old"
    return new > old
  def now(self, oneTwo,one,two)  :
    "return the expected value sum of square deltas"
    n1 = one.n    ; mu1 = one.mu()
    n2 = two.n    ; mu2 = two.mu()
    n  = oneTwo.n ; mu  = oneTwo.mu()
    return n1/n*(mu - mu1)**2 + n2/n*(mu - mu2)**2
 
class RC(R):
  def __init__(self,data, cohen=0.3) :
    "bigEffect is 0.3*standard deviation of all data"
    overall = reduce(lambda x,y: x+y,data)
    self.bigEffect = overall.stdev()*cohen
  def different(self,one,two):
    "is the delta between the means really different?"
    return abs(one.mu() - two.mu()) >= self.bigEffect
