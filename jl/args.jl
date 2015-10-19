# macro sets(f)
#     println(f.args[1])
#     pairs = [x for x in f.args[1].args]
#     ex = [
#               :(it.$(x.args[1]) = $(x.args[2]))
#           for x in pairs]
   
#     :( $ex
#        )
# end

# @sets function aa(aa=1,bb=2)
#     if asd
#         return 2
#     end
#     return 1
# end

@has(aa,bb=1,cc=2)

println(aa0(cc=100))
