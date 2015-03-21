BEGIN {
  Lite = init("_=em `=tt *=b",Lites)
  init("head=head.html neck=neck.html "\
       "foot=foot.html base=timm/15/markdow",
       Parts)
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

ends["0","p"] = "<p>"
ends["p","h"] = ""
ends["u","h"] = "</ul>"
ends["d","h"] = "</dl>"
ends["o","h"] = "</ol>"

     
function markdow(     i,n,lines,line) {
  n = split($0,lines,"\n")
  last="0"
  for(i=1;i<=n;i++)  {
    line = lines[i]
    if (line)
        print inline(line)
    else
        print "<P>"
  }
}
function inline(str,
                x,after,b4,out,i,pat,here,        \
                more,link,url,txt,img,linkp,q) {
  linkp="(!)?\\[([^\\]]+)\\]\\(([^\\)]+)\\)"
  q="\""
  while (match(str,linkp,x)) {
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
