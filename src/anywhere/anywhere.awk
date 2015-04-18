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
  c  = dist(e,w,m,d) + 0.000001
  se = fromHell(e,m,d)
  sw = fromHell(w,m,d)
  if (sw > se) { 
    # swap the ends
    tmp = e ; e  = w;  w  = tmp
    tmp = se; se = sw; sw = tmp 
  }
  for(i in d) {
    if (i == e) continue
    if (i == w) continue
    a = dist(i,e,m,d)
    b = dist(i,w,m,d)
    x = (a**2 + c**2 - b**2) / (2*c)
    hypotenuse = a**2 >= x**2 ? a : b
    y = (hypotenuse**2 - x**2 + 0.00001)**0.5
    nudge(push,m,d,e,i,n,(se-sw)/(y*c))
}}
function nudge(push,m,d,e,i,n,weight,   
               ex,ix,col,mutation,direction,inc) {
  for (col in m["indep"]) 
    if (nump(col,m)) {
      ex = d[e][col]  
      ix = d[i][col]
      if (ix != ex) {
        mutation  = norm(rand()*abs(weight*(ex - ix)),col,m)
        direction = ex < ix ? -1 : 1
        inc = direction*mutation/n
        push[i][col] +=  inc
}}}
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