--unction lines(str)
--   local t = {}
--   local function helper(line)
--      table.insert(t, line)
--      return ""
--   end
--   helper((str:gsub("(.-)\r?\n", helper)))
--   return t
--end
--
--ocal function getfilelist()
--   -- would absolute paths be needed?
--   -- local fname = pandoc.system.get_working_directory()
--   local pfile = pandoc.pipe("find", { ".", "-name", "*.md"}, "-print")
--   return pfile
--nd

BulletedList = function (element)
    for i, item in ipairs(element.content) do
      local first = item[1]
      if first and first.t == 'Plain' then
        element.content[i][1] = pandoc.Para{pandoc.Strong(first.content)}
      end
    end
    return element
  end

--function Pandoc(doc)
--    local hblocks = {}
--    for i,el in pairs(doc.blocks) do
--        if (el.t == "BulletList") then
--            for i, item in ipairs(el.content) do
--                print (el.content[i].t)
--            end
--        end
--    end
--end

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



