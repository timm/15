# next:
# nested lists
# table of contents
# refs
# tables
# read magic vars from line 1
# global abbreviations substituions
# code preformat (python, awk)
# cgi map url into ?
# tables have odd even rows/cols and row0 col0
# fenced code blocks
# highlight
# talk to git
# catch outut to buffer. do subs on buffer. e.g. title

###################################################
## this code recognizes the following markdown 

BEGIN {
  InlineElement= "_=em `=tt *=b !!=sup ~~=sub"
  LinkP = "(!)?\\[([^\\]]+)\\]\\(([^\\)]+)\\)"
  ListP = "([ \t]*)(+|[0-9]+.)?(.*$)"
}
function blockTag(a,i,blanks,  n) { 
  if (a[i+1] ~ /^=/)                 return   "h1"
  if (a[i+1] ~ /^-/)                 return   "h2"
  if (a[i+1] ~ /^~/)                 return   "h3"
  if (a[i]   ~ /^$/)                 return "skip"
  if (a[i]   ~ /^(    |\t)[^\+0-9]/) return  "pre"
  if (a[i]   ~ /^[ \t]+\+/)          return   "ul"
  if (a[i]   ~ /^[ \t]+[0-9]./)      return   "ol"
  if (a[i]   ~ /^#/) {
     gsub(/#+[ \t]*$/,"", a[i]) # zap trailing
     return gsub(/#/,"", a[i]) # count leading
  }
  if (a[i] ~ /^[^ \t]/ && blanks)  return "p"
  return "txt" # denotes normal paragraph text
}

##################################################
## misc boring init stuff

BEGIN {
  InLineP = init(InlineElement,ReName)
  init("head=head.html neck=neck.html "         \
       "foot=foot.html base=timm/15/gitdown",
       Parts)
  # read entire file into $0  
  FS = RS = "_____" "_____"
}
{
  gitdown(ext(FILENAME),$0)
}

function ext(f) {
  sub(/^.*\./,"",f)
  return f
}
function init(str,d,     i,n,tmp,sep,out,key){
  n = split(str, tmp, "( |=|\n)")
  for(i=1; i<=n; i+=2) {
    key    = tmp[i]
	  d[key] = tmp[i+1]
	  out    = out sep key
	  sep    = "|"
  }
  return  "(\\\\)?(" out ")"
}

#############################################
## main 
function gitdown(type, str,     i,n,a,env) {
  print "<div class=contents>"
  stack(env)
  n = split(str,a,"\n")
  while (i < n)
      i = git_on_down(a,i,n,env)
  openClose(env)
  print "</div>"
}
function git_on_down(a,i,n,env,
		                 tag,j,todo,skippedLines) {
  do { # step0: skipblanks
     i++
     if (i >= n) return n
     skippedLines++
     tag = blockTag(a,i, skippedLines > 1)
  } while (tag == "skip")
  j = i   # where to get the next line?
  # step1: simplest case
  if (tag == "txt") 
    print inline(a[i]) 
  else {
    todo = tag
    # step2: sometimes, adjust actions
    if ( tag ~ /^[0-9]$/  ) todo = "h" tag 
    if ( tag ~ /^h[123]$/ ) j = i + 1 
    # step3: close old tag and open new
    openClose(env,todo) 
    # step4: call formatters
    #        and maybe call block tag formatters
    if      (tag == "pre")      j= pre(a,i)         
    else if (tag ~ "^(ul|ol)$") j= list(a,i,tag) 
    else    print inline(a[i])
  }
  # step5: broacast what line to process next
  return j
}
function openClose(env,todo) {
  if (! empty(env) )
      print "</" pop(env)">"
  if (todo)
      print "<"  push(env, todo) ">"
}
#############################
### special formaters

## block-level formatters

# pre-formatted lines
function pre(a,i) {
  do
      print a[i++]
  while (a[i])
  return i
}
# nested lists
function list(a,i,tag,
              pat,x,pre,point,line,
              new,last,lvl,lvls,tmp) {
  while (a[i]) {
    match(a[i],ListP,x)
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
    last = new
    i++
  } 
  while(lvl-- > 1) 
    print "</li>"
  return i
}              
## inline formatter

# Handle hyperlinks

function inline(str,
                x,after,b4,out,i,pat,here,
                more,link,url,txt,img) {
  while (match(str,LinkP,x)) {
    here = RSTART
    more = RLENGTH
    url  = "\"" x[3] "\""
    txt  = x[2]
    img  = x[1]
    if (img)
      link = "<img src="url" alt=\""inline1(txt)"\">"
    else
      link = "<a href="url ">" inline1(txt) "</a>"
    b4  = substr(str, 1, here-1)
    out = out inline1(b4) link
    str = substr(str, here + more) 
  }
  return out inline1(str)
}
# Handle italic, bold, typewriter, sub,sup
function inline1(str,
               x,envs,out,b4,on,
               here,more,env,txt,esc) {
  while (match(str,InLineP,x)) {
    here = RSTART
    more = RLENGTH
    esc  = x[1]
    env  = x[2]
    if (esc) 
       txt = env
    else {
       on = envs[env] = 1 - envs[env]
       txt = (on ? "<" : "</") ReName[env] ">"
    }    
    b4  = substr(str, 1, here-1)
    out = out b4 txt
    str = substr(str, here+more)
  }
  return out str
}
#########################
## standard lib stuff

function top(a)    { return a[a[0]] }
function empty(a)  { return a[0]+0 == 0 }
function stack(a)  { a[0]=0 }
function push(a,x) { a[ ++a[0] ] = x ; return x}
function pop(a)    { return a[ a[0]-- ]  }
