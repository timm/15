load(:one,:oneok)

@ok function fred()
    @assert 1==2/"a"
    @assert 3==3
    @assert 4==4
end


_asserts()

