BEGIN { FS=OFS= "," ; srand(1); M[0] = 0}
      {gsub(/ /,""); gsub(/#.*/,"")
       
      }
/^$/  { next}
      {  RECORD(M,D) }
END   { 
  
  anywheres(M,D,20) 
}
function RECORD(M,D,       src,i) {
  for(i=1;i<=NF;i++)
    src[i] = $i
  M[0]++ ? DATA(src,M,D) : META(src,M)   
}   
function META(src,m,   i,tmp) {
  for (i in src) {
    tmp = m["name"][i]=$i
    if (tmp ~ /[\$<>]/)   {
      m["num"][i]
      m["lo"][i] =    10**16
      m["hi"][i] = -1*10**16
    } else {
      m["sym"][i] 
    }
    if (tmp ~ /</)    m["less"][i]
    if (tmp ~ />/)    m["more"][i]
    tmp ~ /[<>!]/ ? m["goal"][i] : m["indep"][i]
}}
function DATA(src,m,d,   i,tmp,n,name) {
  n = m[0] 
  for(i in src) {
    tmp = src[i]
    name = m["name"][i]
    if (tmp ~ /\?/) 
       continue
    d[n][i]= tmp
    if (i in m["num"]) {
      if (tmp > m["hi"][i]) m["hi"][i] = tmp
      if (tmp < m["lo"][i]) m["lo"][i] = tmp
}}}
function any(l) {
  return int(rand()*(length(l))) + 1
}
function anywheres(m,d,n,   i,push) {
  for(i=1; i<=n; i++)
    anywhere(m,d,push,n)
  for (i in push)
    for(j in push[i])
      print push[i][j]
}
function anywhere(m,d,push,n,
                  e,w,s,se,sw,tmp,i,y,
                  a,b,c,x,hypotenuse) {
  do  {
    e = any(d)   # excellent
    w = any(d)   # worse
  } while (e == w) 
  se = fromHell(e,m,d)
  sw = fromHell(w,m,d)
  if (sw > se) 
    here(w,e,sw - se,m,d,push,n)
  else 
    here(e,w,se - sw,m,d,push,n)
}
function here(e,w,better,m,d,push,n,
              i,a,b,c,x,hypotenuse) {
  c = dist(e,w,m,d)
  for(i in d) {
    if (i == e) continue
    if (i == w) continue
    a = dist(i,e,m,d)
    b = dist(i,w,m,d)
    x = (a**2 + c**2 - b**2) / (2*c)
    hypotenuse = a**2 >= x**2 ? a : b
    y = (hypotenuse**2 - x**2 + 0.00001)**0.5
    for (col in m["indep"])
      mutations(m,d,col,i,e,better/(y*c),push,n)
}}
function mutations(m,d,col,i,e,w,push,n, 
                   ex,ix,b4) {
  ex = d[e][col]
  ix = d[i][col] 
  b4 = push[i][col]
  if (ix != ex)
    push[i][col] = mutate(m,col,ix,ex,w,b4)
}
function mutate(m,col,ix,ex,w,b4,
                mutation,direction) {
  if (nump(col,m)) {
      mutation  = abs(weight*(ex - ix))
      direction = ex < ix ? -1 : 1
      return b4 + direction*mutation/n 
    } else 
      if (weight/n > rand())
        return ex
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
function goalp(col,m) { return col in m["goal"] }
function nump(col,m)  { return col in m["num"]  }
function symp(col,m)  { return col in m["sym"]  }
function norm(n,col,m,    hi,lo) { 
  lo = m["lo"][col]
  hi = m["hi"][col]
  return (n - lo)/(hi-lo+0.0001) 
}
function dist(i,j,m,d,    
              col,x,y,n,inc) { 
  for (col in d[i]) {
    if (goalp(col,m))
      continue
    x = d[i][col]
    y = d[j][col]
    if ((x=="?") && (x=="?")) 
      continue
    n++
    if (symp(col,m)) {
      inc += x != y  
    } else {
      if (x != "?")  x = norm(x,col,m)
      if (y != "?")  y = norm(y,col,m) 
      if (x == "?")  x = y < 0.5 ? 1 : 0
      if (y == "?")  y = x < 0.5 ? 1 : 0
      inc += (x-y)**2 
    }}
  return inc**0.5/n**0.5
} 
function round(i) { return int(i+0.5)  }
function abs(n)   { return n >= 0 ? n : -1*n }

function walk_array(arr, name,      i)
{
    for (i in arr) {
        if (isarray(arr[i]))
            walk_array(arr[i], (name "[" i "]"))
        else
            printf("%s[%s] = %s\n", name, i, arr[i])
    }
}