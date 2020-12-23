#!/usr/bin/env ruby
require "paru/filter"

Paru::Filter.run do 
    with "Header" do |header|
        if header.level == 1
            print(header)
            #doc = new_document
            #chapters[titleize(header)] = doc
        end
    end
end

