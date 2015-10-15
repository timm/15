# for x in Task(() -> generator(3))
#macro task(ex)
 #   :(Task(()->$(esc(ex))))
#end

@has(CSV,
     sep       = ',',
     ignoreCol = '?',
     float     = '$',
     less      = '<',
     more      = '>',
     klass     = '!',
     comment   = r"#.*$",
     white     = r"[ \t\r\n]*",
     era       = 256)

@has(table,
     rows=[],
     header=[])

## xxx to do. extract the open file stuff from here
## to a source that knows about files
function rows(csv::CSV, file)
  """return non-empty rows, divided into cells
     on 'csv.sep', with all whitespace
     pruned away, with all broken lines
     joined to the next one."""
  empty(s)        = length(s) == 0
  broken(s)       = s[end] == csv.sep
  nocomment(s)    = replace(s,csv.comment,"")
  nowhitespace(s) = replace(s,csv.white,"")
  prep(s)         = s |> nocomment |> nowhitespace
  function worker(b4 = "",
                  f  = open(file,"r"))
    for line in eachline(f)
      line = prep(line) 
      if empty(line)
        continue
      elseif broken(line) # if ends with "," we'll
        b4 = b4 * line    # need to join it to next                    
      else
        produce( split(b4 * line, csv.sep) )
        b4 = ""
      end end 
    close(f)
  end
  Task(worker)
end

function cols(csv::CSV,src)
  "return columns not labelled ?XXX." 
  function worker(header = [],
                  ln     = consume(src))
    for (n,s) in enumerate(ln)
      if s[1] != csv.ignoreCol
        push!(header,n)
      end end
    for ln in src
      produce([ln[n] for n in header]) 
    end end
  Task(worker)
end

c=CSV0()

for ln in rows(c,"weather.csv")
  println(ln)
end

for ln in cols(c,
                rows(c,"weather.csv"))
    println(ln)
end


