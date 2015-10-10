_loaded = Dict()

println("# Welcome to Raul's Julia (v0.1)")
function load(files...)    
    for file = files
        file="$(file).jl"
        if !get(_loaded,file,false)
            println("# loading $(file) ...")
            _loaded[file]= true
            include(file)       
        end
    end
end

