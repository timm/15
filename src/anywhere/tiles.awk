{ X[++N] = $NF}
END {
  n= asort(X,D)
  q = int(n/10)
  print D[q],D[2*q],D[3*q],D[4*q],D[5*q],D[6*q],D[7*q],D[8*q],D[9*q]
}
