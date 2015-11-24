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
     era       = 256,
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
type FILER has end

function lines(x::STRINGER,src,tmp=[])
  function worker()
    for ch in src
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

function lines(x::FILER,src)
  function worker()
    f = open(src,"r")
    for line in eachline(f)
      produce(line)
    end
    close(f)
  end
  Task(worker)
end

function lines(x::ZIPPER,src)
  zip, file = match(r"(.*\.zip)/(.*)$",src)
  print(zip)
  print(src)
  function worker()
    r = ZipFile.Reader(zip)
    for f in r.files
      if f == file
        for line in eachline(f)
          produce(line)
        end
        break
      end end
    close(r)
  end
  Task(worker)
end



function rows(csv::CSV, file)
  function worker(b4 = "")
    empty(s)     = length(s) == 0
    broken(s)    = s[end] == csv.sep
    nocomment(s) = replace(s,csv.comment,"")
    nowhites(s)  = replace(s,csv.white,"")
    prep(s)      = s |> nocomment |> nowhites
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
  function worker(header = [])
    for ln in rows(csv)
      if header == []
        for (n,s) in enumerate(ln)
          if s[1] != csv.ignoreCol
            push!(header,n)
          end end
      else
        produce([ln[n] for n in header]) 
      end end end
  Task(worker)
end

#c=CSV0(src=FILER("weather.csv"))
#
#for ln in rows(c)
#  println(ln)
#end
#
#for ln in cols(c)
#   println(">==",ln)
#end


