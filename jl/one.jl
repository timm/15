load(:one,:two)

type SA
    epsilon
    era
end
a=Dict
the = a(:epsilon => 1,
        :delta => a(:aa => 2,
                    :bb => 3))

 

 #=
 INPUT:
 #------------------------------
 @def aa bb=1 cc=10+1

 someFun(x::Any) = println(1000000)
 someFun(x::aa)  = println(x.bb)

 x    = aa0()
 x.bb = 200

 someFun(22)
 someFun(x)

 OUTPUT: 
 #------------------------------
 begin
    type aa # /Users/timm/gits/timm/15/jl/one.jl, line 18:
        bb
        cc
    end
    function aa0() # /Users/timm/gits/timm/15/jl/one.jl, line 21:
        aa(1,10 + 1)
    end
 end

 1000000
 200
 
 =#

println(macroexpand(:(@def aa bb=1 cc=10+1)))

@def aa bb=1 cc=10+1

someFun(x::Any) = println(1000000)
someFun(x::aa)  = println(x.bb)

x    = aa0()
x.bb = 200

someFun(22)
someFun(x)
