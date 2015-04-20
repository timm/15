function line(f,   str) {
  if ((getline str < f) > 0) {
    gsub(/[ \t\r]*/,"",str) 
    gsub(/#.*$/,"",str)
    if ( str ~ /,[ \t]*$/ )
      return str line(f)
    else 
      return str 
}}
function readcsv(m,d,f,  str,n) {
  f = f ? f : "/dev/stdin"
  while(str = line(f)) 
     readcsv1(n++, str,",",m,d)
  return n - 1
}
function readcsv1(n,str,fs,m,d,     src) {
  split(str,src,fs)
  n ? data(src,m,d,n) : meta(src,m)
}
function meta(src,m,   i,tmp) {
  for (i in src) {
    tmp = m["name"][i]=src[i]
    if (tmp ~ /[\$<>]/)   {
      m["num"][i]
      m["lo"][i] =    10**32
      m["hi"][i] = -1*10**32
    } else {
      m["sym"][i] 
    }
    if (tmp ~ /</)  m["less"][i]
    if (tmp ~ />/)  m["more"][i]
    tmp ~ /[<>!]/ ? m["goal"][i] : m["indep"][i]
}}
function data(src,m,d,n,   i,tmp) {
  for(i in src) 
    if (src[i] !~ /\?/) { 
      tmp = d[n][i]= src[i]
      if (i in m["num"]) {
        if (tmp > m["hi"][i]) m["hi"][i] = tmp
        if (tmp < m["lo"][i]) m["lo"][i] = tmp
}}}
function goalp(col,m) { return col in m["goal"] }
function nump(col,m)  { return col in m["num"]  }
function symp(col,m)  { return col in m["sym"]  }
function norm(n,col,m,    hi,lo) { 
  lo = m["lo"][col]
  hi = m["hi"][col]
  return (n - lo)/(hi-lo+0.0001) 
}
function wrap(x,lo,hi) {
  if (x > hi) return hi
  if (x < lo) return lo
  return x
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
      inc += x == y ? 0 : 1  
    } else {
      if (x != "?") x = norm(x,col,m)
      if (y != "?") y = norm(y,col,m) 
      if (x == "?") x = y < 0.5 ? 1 : 0
      if (y == "?") y = x < 0.5 ? 1 : 0
      inc += (x-y)**2 
    }}
  return inc**0.5/n**0.5
} 
