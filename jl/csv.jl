# for x in Task(() -> generator(3))

@has(csv,
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
function rows(my::csv, file)
  """return non-empty rows, divided into cells
     on 'my.sep', with all whitespace
     pruned away, with all broken lines
     joined to the next one."""
  empty(s)        = length(s) == 0
  broken(s)       = s[end] == my.sep
  nocomment(s)    = replace(s,my.comment,"")
  nowhitespace(s) = replace(s,my.white,"")
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
        produce( split(b4 * line, my.sep) )
        b4 = ""
      end end 
    close(f)
  end
  Task(worker)
end

function cols(my::csv,src)
  "return columns not labelled ?XXX." 
  function worker(header = [],
                  ln     = consume(src))
    for (n,s) in enumerate(ln)
      if s[1] != my.ignoreCol
        push!(header,n)
      end end
    for ln in src
      produce([ln[n] for n in header]) 
    end end
  Task(worker)
end

c=csv0()

for ln in rows(c,"weather.csv")
  println(ln)
end

for ln in cols(c,
                rows(c,"weather.csv"))
    println(ln)
end


