@include "lib.awk"
@include "table.awk"

BEGIN { 
 f="weather.csv"
 readcsv(f,m,d)
 o(d,"data")
 exit
 anywhere(m,d,p,20)
}
function anywhere(m,d,p,n,   
                  max,order,i,j,e,w,c,se,sw) {
  max = anys(d,order)
  for(i=1; i<=n; i+=2) {
     e  = order[i]
     w  = order[i] + 1
     c  = dist(e,w,m,d) + 0.00001
     se = fromHell(e,m,d)
     sw = fromHell(w,m,d)
     for(j=n+1; j<=max; j++) {
       if (sw > se) 
          here(m,d,w,e,c,order[j],sw,se,p)
       else 
          here(m,d,e,w,c,order[j],se,sw,p)
}}}
function here(m,d,e,w,c,i,se,sw,p,
              ex,ix,col,a,b,x,hypotenuse,y) { 
  a = dist(i,e,m,d)
  b = dist(i,w,m,d)
  x = (a**2 + c**2 - b**2) / (2*c)
  hypotenuse = a**2 >= x**2 ? a : b
  y = (hypotenuse**2 - x**2)**0.5
  p[i] = (b/c)*(se-sw)/(c*y**2)
  for (col in m["indep"]) {
    ex = d[e][col]
    ix = d[i][col]  
    if (ix != ex) 
      d[i][col] = nudge(m,col,ix,ex,p[i])
}}
function nudge(m,col,ix,ex,want,
                mutation,direction) {
  if (nump(col,m)) {
      mutation  = abs(want*(ex - ix))
      direction = ex < ix ? -1 : 1
      return b4 + direction*mutation/n 
    } else 
      return want > rand() ? ex : ix
}
function fromHell(i,m,d,   
                  col,n,x,hell,inc,more) {
  for (col in m["goal"]) {
    n++
    x    = d[i][col]
    x    = norm(x,col,m)
    hell = col in more ? 0 : 1
    inc += (x - hell)**2  
  }
  return inc**0.5/n**0.5
}