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
     era       = 256
     src       = STRINGER(""))

@has(table,
     rows=[],
     header=[])

## xxx to do. extract the open file stuff from here
## to a source that knows about file

#@doc """return non-empty rows, divided into cells
#  on 'csv.sep', with all whitespace pruned away, 
#  with all broken lines joined to the next one 
#  """ ->

type ZIPPER has  end
type STRINGER has end

function lines(x::STRINGER,tmp=[])
  function worker()
    for ch in x.has
      if ch == '\n'
        produce(string(tmp...))
        tmp=[]
      else
        push!(tmp,ch)
      end
      if length(tmp) > 0
        produce(string(tmp...))
      end end end
  Task(worker)
end

function lines(x::FILER)
  function worker()
    f = open(x.has,"r")
    for line in eachline(f)
      produce(line)
    end
    close(f)
  end
  Task(worker)
end
      
function rows(csv::CSV, file)
  function worker()
    empty(s)     = length(s) == 0
    broken(s)    = s[end] == csv.sep
    nocomment(s) = replace(s,csv.comment,"")
    nowhites(s)  = replace(s,csv.white,"")
    prep(s)      = s |> nocomment |> nowhites
    b4 = ""
    for line in csv.src
      line = prep(line) 
      if empty(line)
        continue
      elseif broken(line) # if ends with "," we'll
        b4 = b4 * line    # need to join it to next                    
      else
        produce( split(b4 * line, csv.sep) )
        b4 = ""
      end end end
  Task(worker)
end

function cols(csv::CSV)
  function worker()
    header = []
    ln     = consume(csv.src)
    for (n,s) in enumerate(ln)
      if s[1] != csv.ignoreCol
        push!(header,n)
      end end
    for ln in src
      produce([ln[n] for n in header]) 
    end end
  Task(worker)
end

c=CSV0(src=FILER("weather.csv"))

for ln in rows(c)
 println(ln)
end

for ln in cols(c,
               rows(c,"weather.csv"))
   println(">==",ln)
end


