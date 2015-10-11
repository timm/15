#=
These is Raul's tweaks of Julia.

Raúl Rafael Juliá y Arcelay (March 9, 1940 – October
24, 1994) was a Puerto Rican actor.  Born in San
Juan, he gained interest in acting while still in
school. Upon completing his studies, Juliá decided
to pursue a career in acting.

After gaining visibility, he received roles in two
television series, Love of Life and Sesame
Street.  Between 1974 and 1982, Juliá received
Tony Award nominations for Where's Charley?, The
Threepenny Opera and Nine. During the 1980s, he
worked in several films, receiving nominations
for the Golden Globe Awards, for his performance
in Tempest, and Kiss of the Spider Woman,
winning the National Board of Review Award for
Best Actor for the latter.

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

println("# Welcome to Raul's Julia (v0.1)")

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
# test engine

_tries = 0
_fails = 0

# if crash or fails, _fails += 1
macro assert(ex)
    :(global _tries,_fails;
      _tries += 1;
      try    
        if ! $ex
          _fails += 1
          println(string("Assertion failed: ",$(string(ex))))
        end
      catch e
        _fails += 1
        println(string("Exception: ",$(string(ex))))
      end)
end    

# report results
function _asserts()
    global _tries,_fails
    println("Pass: $(_tries - _fails); Fails: $_fails")
end

# function prefix, auto run on load
macro ok(ex)
    :($ex; $(ex.args[1]))
end

