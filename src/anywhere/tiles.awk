BEGIN{ F=5}
{ X[++N] = $NF}
function g(n) { return sprintf("%."F"f",D[n]) }
END {
  n= asort(X,D)
  q = int(n/10)
  print g(q),g(2*q),g(3*q),g(4*q),g(5*q),\
        g(6*q),g(7*q),g(8*q),g(9*q)
}
