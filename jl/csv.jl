include("load.jl"
function csv(file)
    open(file,"r") do f
        for line in eachline(f)
            println("read line: ", line)
        end
    end
end

