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
function anywhere(m,d,n,   i,push) {
  max = shuffle(d)
  for(e=1; e<=n; e+=2) {
     w  = e + 1
     c  = dist(e,w,m,d) + 0.00001
     se = fromHell(e,m,d)
     sw = fromHell(w,m,d)
     for(i=n+1;i<=max;i++) {
       if (sw > se) 
          here(m,d,w,e,c,i,sw,se)
       else 
          here(m,d,e,w,c,i,se,sw)
}}}
function here(m,d,e,w,c,i,se,sw,
              ex,ix,col,a,b,x,hypotenuse,y) { 
  a = dist(i,e,m,d)
  b = dist(i,w,m,d)
  x = (a**2 + c**2 - b**2) / (2*c)
  hypotenuse = a**2 >= x**2 ? a : b
  y = (hypotenuse**2 - x**2)**0.5
  for (col in m["indep"]) {
    ex = d[e][col]
    ix = d[i][col]  
    if (ix != ex) 
      d[i][col] = nudge(m,col,ix,ex,
                        (b/c)*(se-sw)/(c*y)) #??? b/c
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

function shuffle(a,  i,j,n,tmp) {
  n = length(a) 
  for(i=1;i<=n;i++) {
    j = i + round(rand()*(n-i));
    tmp=a[j];
    a[j]=a[i];
    a[i]=tmp;
  };
  return n;
}
function round(x) { return int(x + 0.5) }