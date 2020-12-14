local function split(str,pat)
    local tbl = {}
    str:gsub(pat, function(x) tbl[#tbl+1]=x end)
    return tbl
 end
 
 local str = "a,,b\nc"     -- comma-separated list
 local pat = "\n"    -- everything except commas
 assert (table.concat(split(str, pat), ",") == str)
 tbl = split(str,pat)
 print(tbl[1]) 