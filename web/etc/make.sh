etc="$1"
f="$2"
title=$(head -1 "$f")
(head="$title" bash "$etc"/head.sh
 tail -n +2 "$f" 
 bash "$etc"/tail.sh) #|
#tidy5 -q -errors /dev/null -config "$etc"/tidy.cfg
