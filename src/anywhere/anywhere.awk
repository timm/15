BEGIN { FS=OFS= "," ; srand(1)}
{gsub(/ /,"")
 gsub(/#.*/,"")
}
/^$/ { next}
     { N++ ? DATA() | NAMES() }
END  { anywhere() }

function NAMES(   i,tmp) {
  for{i=1;i<=NF;i++) {
    tmp = Name[i]=$i
    if (tmp ~ /\$/) Num[i]
    if (tmp ~ /</)  Less[i]
    if (tmp ~ />/)  More[i]
}}
function DATA(n,l,   i,tmp) {
  for(i=1;i<=NF;i++) {
    tmp = $i
    if (tmp ~ /\?/) 
       continue
    l[n][Name[i]]= tmp
    if (i in Num) {
      if (! (i in Hi)) 
        Hi[i] = Lo[i] = tmp
      else {
        if (tmp > Hi[i]) Hi[i] = tmp
        if (tmp < Lo[i]) Ko[i] = tmp
}}}}
function any(l) {
  return round(rand()*length(l))
}
function anywhere(data,names,n,
                  i,j) {
  repeat 
    i = any(data)
    j = any(data)
  until (i != j) 
}
function norm(i,lo,hi) { return (i-lo)/(hi-lo+0.0001) }
function dist(i,j,data,     c,x,y,n,inc) { 
  for (c in data[i]) {
    x = data[i][c]
    y = data[j][c]
    if ((x=="?") && (x=="?")) 
      continue
    n++
    if (! (c in Num))
      inc += x==y ? 0 : 1
    else {
      if (x != "?")  x = norm(x,Lo[c],Hi[c])
      if (y != "?")  y = norm(y,Lo[c],Hi[c])
      if (x == "?")  x = y < 0.5 : 1 : 0
      if (y == "?")  y = x < 0.5 : 1 : 0
      inc += (x-y)**2 
    }}
  return inc**0.5/n**0.5
} 

function round(i) { return int(i+0.5) }