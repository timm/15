function max(i,j) { return i > j ? i : j }
function min(i,j) { return i < j ? i : j }
function a(l)     { split("",l,"") }
function round(i) { return int(i+0.5) }
function abs(n)   { return n >= 0 ? n : -1*n } 
function any(l)   {
  return int(rand()*(length(l))) + 1
}
function anys(lst0,lst,   i) {
  for(i in lst0)
      lst[i] = i
  return shuffle(lst)
}
function isnum(x) { 
  return x=="" ? 0 : x == (0+strtonum(x)) 
}
function o(l,prefix,order,   indent,   old,i) {
  if(! isarray(l)) {
    print "not array",prefix,l
    return 0}
  if(!order)
    for(i in l) { 
      order= isnum(i) ? "@ind_num_asc" : "@ind_str_asc"
      break
    }     
   old = PROCINFO["sorted_in"] 
   PROCINFO["sorted_in"]= order
   for(i in l) 
     if (isarray(l[i])) {
       print indent prefix "[" i "]"
       o(l[i],"",order, indent "|   ")
     } else
       print indent prefix "["i"] = (" l[i] ")"
   PROCINFO["sorted_in"]  = old 
}
function shuffle(a,  i,j,n,tmp) {
  n = length(a)
  for(i=1;i<=n;i++) {
    j=i+round(rand()*(n-i));
    tmp=a[j];
    a[j]=a[i];
    a[i]=tmp;
  };
  return n;
}
