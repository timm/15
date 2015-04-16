BEGIN { FS=OFS= "," ; srand(1)}
{gsub(/ /,"")
 gsub(/#.*/,"")
}
/^$/ { next}
     { ROW(Src,NF)
       M[0]++ ? DATA(SRC,M,D) | NAMES(SRC,M) }
END  { anywhere(M,D) }

function ROW(l,n,   i) {
  split("",l,"")
  for(i=1;i<=n;i++)
    l[i] = $i
}
function NAMES(src,m,   i,tmp) {
  for{i=src) {
    tmp = m["name"][i]=$i
    if (tmp ~ /\$/)   m["num"][i]
    if (tmp ~ /</)    m["less"][i]
    if (tmp ~ />/)    m["more"][i]
    if (tmp ~ /[<>]/) m["goal"][i] 
}}
function DATA(src,m,d,   i,tmp) {
  n = m[0]
  for(i in src) {
    tmp = src[i]
    name = m["name"][i]
    if (tmp ~ /\?/) 
       continue
    d[n][i]= tmp
    if (i in m["num"]) {
      if (! (i in n["lo"])) 
        m["lo"][i] = m["hi"][i] = tmp
      else {
        if (tmp > m["hi"][i]) m["hi"][i] = tmp
        if (tmp < m["lo"][i]) m["lo"][i] = tmp
}}}}
function any(l) {
  return round(rand()*length(l))
}
function anywhere(d,m,
                  i,j) {
  repeat 
    i = any(d)
    j = any(d)
  until (i != j) 
  c = dist(i,j,m,d)
  for(k in d) {
    a= dist(k,i,m,d)
    b= dist(l,j,m,d)
    x= (a**2 + c**2 - b**2) / (2*a*c)
    if (x >= 0) && (x <= 1) {
       y = (a**2 - x**2)**0.5
       
    }
  }
}
function goalp(i,m)    { return i in m["goal"] }
function nump(i,m)     { return i in m["num"] }
function symp(i,m)     { return i in m["num"] ? 0 : 1 }
function norm(n,i,m)   { 
  lo = m[i]["lo"] 
  hi = m[i]["hi"]
  return (n-lo)/(hi-lo+0.0001) 
}
function dist(i,j,m,d    col,x,y,n,inc) { 
  for (col in d[i]) {
    if (goalp(col,m))
      continue
    x = d[i][col]
    y = d[j][col]
    if ((x=="?") && (x=="?")) 
      continue
    n++
    if (symp(col,m))
      inc += x==y ? 0 : 1
    else {
      if (x != "?")  x = norm(x,col,m)
      if (y != "?")  y = norm(y,col,m) 
      if (x == "?")  x = y < 0.5 : 1 : 0
      if (y == "?")  y = x < 0.5 : 1 : 0
      inc += (x-y)**2 
    }}
  return inc**0.5/n**0.5
} 

function round(i) { return int(i+0.5) }