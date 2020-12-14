function lines(str)
    local t = {}
    local function helper(line)
       table.insert(t, line)
       return ""
    end
    helper((str:gsub("(.-)\r?\n", helper)))
    return t
 end

local function getfilelist()
    -- would absolute paths be needed?
    -- local fname = pandoc.system.get_working_directory()
    local pfile = pandoc.pipe("find", { ".", "-name", "*.md"}, "-print")
    return pfile
end

function Pandoc(doc)
    local hblocks = {}
    for i,el in pairs(doc.blocks) do
        if (el.t == "BulletList") then
           --table.insert(hblocks, [Header 1 ('document-tree',[],[]) [Str 'Document',Space,Str 'Tree']])
           return el
        end
    end
end

--function Blocks(block)
--    -- Go from end to start to avoid problems with shifting indices.
--    for i = #blocks-1, 1, -1 do
--      if (i == 3) then
--        return block
--      end
--      
--    end
--    --return blocks
--  end
  
--function Pandoc(doc)
--    local hblocks = {}
--    for i,el in pairs(doc.blocks) do
--        if (el.t == "Div" and el.classes[1] == "handout") or
--           (el.t == "BlockQuote") or
--           (el.t == "UnorderedList") or
--           (el.t == "Para" and #el.c == 1 and el.c[1].t == "Image") or
--           (el.t == "Header") then
--           table.insert(hblocks, el)
--        end
--    end
--    return pandoc.Pandoc(hblocks, doc.meta)
--end



