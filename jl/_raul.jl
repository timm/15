println("# Welcome to Raul's Julia (v0.1)")

#=
These is Raul's tweaks of Julia.

## Usage:

    julia --load _raul.jl theRestOfYour code

## Examples:

For exampls of the `@ok` and `@spy` macro, see

    https://github.com/timm/15/blob/master/jl/oneok.jl

For examples of `load` function, see the following files.
Note that they contain an `include` loop, which `load`
fixes.
    
    https://github.com/timm/15/blob/master/jl/one.jl
    https://github.com/timm/15/blob/master/jl/two.jl
    https://github.com/timm/15/blob/master/jl/three.jl

## Why is this called Raul? 

I'm glad you asked.  Raúl Rafael Juliá y Arcelay
(March 9, 1940 – October 24, 1994) was a Puerto
Rican actor.  He received roles in two television
series, Love of Life and Sesame Street.  Between
1974 and 1982, Juliá received Tony Award nominations
for Where's Charley?, The Threepenny Opera and
Nine. During the 1980s, he worked in several films,
receiving nominations for the Golden Globe Awards,
for his performance in Tempest, and Kiss of the
Spider Woman, winning the National Board of Review
Award for Best Actor for the latter.

In 1991 and 1993, Juliá portrayed Gomez Addams
in two film adaptations of The Addams Family. In
1994, he filmed The Burning Season, for which he
won a Golden Globe Best Actor award, and a film
adaptation of the Street Fighter video
games. Later that year, Juliá suffered several
health afflictions, eventually dying after
suffering a stroke. His funeral was held in
Puerto Rico, being attended by thousands. For
his work in The Burning Season, Juliá won a
posthumous Golden Globe and Emmy Award.

=#        

#------------------------------------
# repeated includes only include once

_loaded = Dict()

function load(files...)
    for file = files
        file="$(file).jl"
        if !get(_loaded,file,false)
            println("# loading $(file)")
            _loaded[file]= true
            include(file)       
        end
    end
end 

#------------------------------------
# function prefix, auto run on load

macro spy(ex)
    local what=ex.args[1].args[1]
    :($ex;
      println(string("\n# ", $(string(what))));
      $(ex.args[1]))
end

#------------------------------------------------
# test engine
# Keeps a global count of all tries and failes.
# Also, programming exceptions don't stop the tests.

_tries = 0
_fails = 0

# if crash or fails, _fails += 1
macro ok(ex,msgs...)
    msgs = string(isempty(msgs) ? ex : msgs[1])
    :(global _tries,_fails;
      _tries += 1;
      try    
        if ! $ex
          _fails += 1
          println(string("Assertion failed: ",$(msgs)))
        end
      catch e
        _fails += 1
        println(string("Exception: ",$(msgs)))
      end)
end    

# report results
function oks()
    global _tries,_fails
    println("Pass: $(_tries - _fails); Fails: $_fails")
end


