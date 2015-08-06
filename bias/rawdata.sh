data() {
  cat rawdata.txt
}
data #|
#gawk -F, '{
 #    OFS=","
  #   q=","
   #  print $1,$2,$3,$4,q $5 q,q $6 q, q $7 q,$8
    # }'
