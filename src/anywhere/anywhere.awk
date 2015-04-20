@include "lib.awk"
@include "table.awk"

BEGIN { main() }

function main(   n,m,d,p) {
    srand(1)
    n = readcsv(m,d)
    anywhere(m,d,p,
             n < 50 ? 10 : 20)
    #o(p,"p")
}
function anywhere(m,d,p,n,   
                  max,order,i,j,e,w,c,se,sw,l) {
  max = anys(d,order)
  for(i=1; i<=n; i+=2) {
     e  = order[i]
     w  = order[i+1]
     c  = dist(e,w,m,d) + 0.00001
     se = fromHell(e,m,d)
     sw = fromHell(w,m,d)
     for(j=n+1; j<=max; j++) {
       if (sw > se) 
          here(m,d,w,e,c,sw,se,p,n,order[j])
       else 
          here(m,d,e,w,c,se,sw,p,n,order[j]) }}}
function  here(m,d,e,w,c,se,sw,p,n,i,
               ex,ix,col,a,b,x,y,inc) {
  a = dist(i,e,m,d)
  b = dist(i,w,m,d)
  x = (a**2 + c**2 - b**2) / (2*c)
  if (x > c || x > a) return 0
  y = (a**2 - x**2)**0.5
  p[i] = inc = a/b*(se-sw)/(c*y**2)/n
  #p[i] = inc
  print e,w,i,a,b,c,x,y,se,sw,inc
  for (col in m["indep"]) {
    ex = d[e][col]
    ix = d[i][col]  
    if (ix != ex) 
      d[i][col] = nudge(m,col,ix,ex,p[i])
}}
function nudge(m,col,ix,ex,want,
               mutation,direction,out,new) {
  if (nump(col,m)) {
      mutation  = abs(want*(ex - ix))
      direction = ex < ix ? -1 : 1
      new = ex + direction*mutation
      out =  wrap(new,
                  m["lo"][col],
                  m["hi"][col])
      #print col,ex,out,int(100*(ex-out)/(ex + 0.0001))
    } else 
      out = want > rand() ? ex : ix
  
  return out
}
function fromHell(i,m,d,   
                  col,n,x,x1,hell,inc,more) {
  for (col in m["goal"]) {
    n++
    x = d[i][col]
    x1 = norm(x,col,m)
    hell = col in more ? 0 : 1
    inc += (x1 - hell)**2  
  }
  return inc**0.5/n**0.5
}
