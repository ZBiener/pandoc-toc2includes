local function getfilelist()
    local fname = pandoc.system.get_working_directory()
    local dirname = fname .. "/*.*"
    print(dirname)
    local pfile = pandoc.pipe("find", { ".", "-name", "*.md"}, "-print")
    return pfile
end

function Meta(m)
    filelist = getfilelist()
    print(filelist)
    return filelist
end





