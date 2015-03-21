BEGIN {
  Lite = init("_=em `=tt *=b",Lites)
  init("head=head.html neck=neck.html "\
       "foot=foot.html base=timm/15/markdow",
       Parts)
  Linkp="(!)?\\[([^\\]]+)\\]\\(([^\\)]+)\\)"
}
BEGIN {
  FS = RS = "_____" "_____"
  getline
	markdow()
}
function init(str,d,     i,n,tmp,sep,out,key){
  n = split(str, tmp, "( |=|\n)")
  for(i=1; i<=n; i+=2) {
    key    = tmp[i]
	  d[key] = tmp[i+1]
	  out    = out sep key
	  sep    = "|"
  }
  return  "(" out ")"
}     
function markdow(     i,n,lines,blanks,last) {
  n = split($0,lines,"\n")
  last=""
  for(i=i;i<=n;i++)  {
    line = lines[i]
    now = what(line)
    if (now=="blank") {
       blanks++
       continue
    } else {
        eblanks=0
        finish(last,now,blanks)
    
        finish(last,"pre")
        i += pre(lines)
        last = "pre"
        continue
    }
    last = now 
    last = worker(lines[i],blanks,last)
  }
}
function what(line) {
  if (line       ~ /^$/)                 return "blank"
  if (line       ~ /^(    |\t)[^\+0-9]/) return "pre"
  if (line       ~ /^(    |\t)\+/)       return "ul"
  if (line       ~ /^(    |\t)[0-9]/)    return "ol"
  if (line       ~ /^#/)                 return "inhead"
  if (lines[i+1] ~ /^=/)                 return "h1"
  if (lines[i+1] ~ /^-/)                 return "h2"
  if (lines[i+1] ~ /^~/)                 return "h3"
  return "p"
}    
function inline(str,
                x,after,b4,out,i,pat,here,        \
                more,link,url,txt,img,linkp,q) {
  q="\""
  while (match(str,Linkp,x)) {
    here = RSTART
    more = RLENGTH
    url  = x[3]
    txt  = x[2]
    img  = x[1]
    b4   = substr(str, 1, here-1)
    if (img)
      link = "<img src="q url q" alt=\""txt"\">"
	  else
	    link = "<a href="q url q">" lites(txt) "</a>"
	  out = out lites(b4) link
	  str = substr(str, here + more) 
  }
  return out lites(str)
}
function lites(str,
               x,envs,out,b4,pre,here,more,env) {
  while (match(str,Lite,x)) {
    here = RSTART
    more = RLENGTH
    env  = x[1]
    pre  = envs[env] = 1 - envs[env]
    pre  = pre ? "<" : "</"
    b4   = substr(str, 1, here-1)
    out  = out b4 pre Lites[env] ">"
    str  = substr(str, here+more)
  }
  return out str
}
