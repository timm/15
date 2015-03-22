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
	gitdown()
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
function gitdown(     i,n,lines,blanks,last) {
  stack(Finish)
  push(Finish,"")
  n = split($0,lines,"\n")
  inList=0
  while (i < n) {
    do
      i++
      now = what(lines,i,blanks)
    while (now == "blanks") 
    if (now=="pre") {
       block("pre")
       i = pre(lines,i,n)
       continue
    }
    if (now ~ "^(ul|ol)$") {
       block(now)
       i = list(lines,i,n,now)
       continue
    } else if (now ~ /[123]/) {
        block("h" now)
        i++
    } else
        block(now)
    print inline(lines[i])
  }
}
function list(lines,i,n,tag,
              pat,x,pre,point,line,
              now,last,lvls,tmp) {
  pat = "([ \t]*)(\+|[0-9]*\.)?(.*$)"
  while (1) {
    match(lines[i],pat,x)
    pre   = x[1]
    point = x[2]
    line  = inline(x[3])
    new   = sub(/[ \t]*/,"",pre) + 1
    if (new == last) {
        print "</li><li>"
    } else if (new > last) {
        print "<" tag "><li>"
        lvls[new] = ++lvl
    } else if (new in lvls) {
        tmp = lvls[new]
        while(lvl-- > tmp) 
          print "</li></" tag ">"
        print "<li>"
    }
    print line
    last = now
    i++
  }
  while(lvl-- > 1) 
    print "</li></" tag ">"
  return i
}              
function pre(lines,i,n) {
  do
    print lines[i]
    i += 1
  while (i<=n && lines[i])
  return i
}
function block(what,whatnext) {
  whatnext = whatnext ? whatnext : what
  printf("</%s>", pop(Finish))
  push(Finish, whatnext)
  print "<" what ">"
}
function stack(x)  { x[0]=0 }
function top(x)  { return x[x[0]] }

function push(a,x) { a[++a[0]] = x }
function pop(a)    { return a[a[0]--]  }

function what(lines,i,blanks,     line) {
  line = lines[i]
  if (line       ~ /^$/)                 return "blank"
  if (line       ~ /^(    |\t)[^\+0-9]/) return "pre"
  if (line       ~ /^(    |\t)\+/)       return "ul"
  if (line       ~ /^(    |\t)[0-9]/)    return "ol"
  if (line       ~ /^#/)                 return hn(lines,i)
  if (lines[i+1] ~ /^=/)                 return "h1"
  if (lines[i+1] ~ /^-/)                 return "h2"
  if (lines[i+1] ~ /^~/)                 return "h3"
  if (blanks > 0 )                       return "p"
  return ""
}
function hn(lines,i) {
  gsub(/#*[ \t]*$/,"", lines[i])
  return gsub(/^#+/,"", lines[i])
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
