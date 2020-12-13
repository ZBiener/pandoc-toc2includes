function Doc(e)
    local fname = pandoc.system.get_working_directory() .. "/*.md"
    print(fname)
    local pfile = pandoc.pipe("ls", {"-al"}, fname)
    --for filename in pfile:lines() do
    --    i = i + 1
    --    --t[i] = filename
    --    str = str + " " + filename
    -- end
    print(pfile)
end




