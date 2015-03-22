# next:
# all the text not bold again
# escapes for special characters
# super script subscript
# nested lists
# refs
# tables

###################################################
## this code recognizes the following markdown 

InlineElement= "_=em `=tt *=b"
Linkp        = "(!)?\\[([^\\]]+)\\]\\(([^\\)]+)\\)"
Listp        = "([ \t]*)(+|[0-9]+.)?(.*$)"

function blockElement(a,i,blanks) {
  if (a[i+1] ~ /^=/)                    return "h1"
  if (a[i+1] ~ /^-/)                    return "h2"
  if (a[i+1] ~ /^~/)                    return "h3"
  if (a[i]   ~ /^$/)                  return "skip"
  if (a[i]   ~ /^(    |\t)[^\+0-9]/)   return "pre"
  if (a[i]   ~ /^[ \t]+\+/)             return "ul"
  if (a[i]   ~ /^[ \t]+[0-9]./)         return "ol"
  if (a[i]   ~ /^[A-Za-z0-9]/ && blanks) return "p"
  if (a[i]   ~ /^#/) {
      gsub(/#*[ \t]*$/,"", a[i]) # zap trailing #
      return gsub(/^#+/,"", a[i])# count leadning #
  }
  return "" # denotes normal paragraph text
}

##################################################
## misc boring init stuff

BEGIN {
  Lite = init(InlineElement,Lites)
  init("head=head.html neck=neck.html "\
       "foot=foot.html base=timm/15/markdow",
       Parts)  
  # read entire file into $0
  FS = RS = "_____" "_____"; getline
  gitdown($0)
}

function init(str,d,     i,n,tmp,sep,out,key){
  n = split(str, tmp, "( |=|\n)")
  for(i=1; i<=n; i+=2) {
    key    = tmp[i]
	  d[key] = tmp[i+1]
	  out    = out sep key
	  sep    = "|"  }
  return  "(" out ")"
}

#############################################
## main 
function gitdown(str,
                 i,n,a,env) {  
  print "<div class=contents>"
  stack(env)
  n = split(str,a,"\n")
  while (i < n)
      i = git_on_down(a,i,env)
  if (! empty(env) && top(env) )
      print("<%s>",pop(env))
  print "</div>"
}

function git_on_down(a,i,env,
		element,j,todo,skippedLines) {
  # step1: skipblanks
  skippedLines = -1 # True after two do-whiles
  do { 
     i++
     skippedLines++
     element = blockElement(a,i, skippedLines)
  } while (element=="skip")
  
  # step2: set standard actions
  todo = element   # what is the current line?
  j    = i + 1     # where is the next line?

  # step3: sometimes, adjust actions
  if (element ~ /^[0-9]$/ )
      todo = "h" element 
  else if (element ~ /^h[123]$/)
      j = i + 2 # i.e. skip a line
  ;
  # step4: close old element and open new
  if (! empty(env) )
      print "</" pop(env)">"
  print "<"  push(env, todo) ">"
  
  # step5: call formatters
  # step5a: maybe call block element formatters
  if (element == "pre") 
      j = pre(a,i)         
  else if (element ~ "^(ul|ol)$")
      j = list(a,i,element) 
  else # step5b: else call inline formatter
      print inline(a[i])
  ;
  # step6: broacast what line to process next
  return j
}


#############################
### special formaters

## block-level formatters

# pre-formatted lines
function pre(a,i) {
  do print a[i++] while (a[i])
  return i
}
# nested lists
function list(a,i,element,
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
        print "<" element "><li>"
        lvls[new] = ++lvl
    } else if (new in lvls) {
        tmp = lvls[new]
        while(lvl-- > tmp) 
          print "</li></" element ">"
        print "<li>"
    }
    print line
    last = new
    i++
  } 
  while(lvl-- > 1) 
    print "</li></" element ">"
  return i
}              
## inline formatter

# Handle hyperlinks
function inline(str,
                x,after,b4,out,i,pat,here,        \
                more,link,url,txt,img,linkp,q) {
  q="\""
  while (match(str,Linkp,x)) {
    here = RSTART
    more = RLENGTH
    url  = q x[3] q
    txt  = x[2]
    img  = x[1]
    b4   = substr(str, 1, here-1)
    if (img)
      link = "<img src="url" alt=\""txt"\">"
    else
      link = "<a href="url ">" lites(txt) "</a>"
    out = out lites(b4) link
    str = substr(str, here + more) 
  }
  return out lites(str)
}
# Handle italic, bold, typewriter fonr
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
#########################
## standard lib stuff

function empty(a)  { return a[0] == 0 }
function stack(a)  { a[0]=0 }
function push(a,x) { a[ ++a[0] ] = x ; return x}
function pop(a)    { return a[ a[0]-- ]  }
