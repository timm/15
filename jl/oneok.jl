load(:one)

@spy function fred()
    @ok 2==1 
    @ok 3==3/"a"
    @ok 4==4
end

#_asserts()

d1=Dict()

d1[:a] =  Dict(:A => "alpha")

function of(d,keys...)
    out=d
    for key=keys
        out = out[key]
    end
    out
end

Base.call(x::Number, arg) = x * arg

println(o(d1,a,A))



