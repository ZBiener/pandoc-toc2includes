#!/usr/bin/env ruby
# If we have abstract: metadata, convert it to an
# "Abstract: " paragraph at the start of the document
# This is because some templates / plain text cannot handle this natively
#
# VERSION: 1.0.0

require 'paru/filter'


Paru::Filter.run do
  dirs = Dir.glob("*.md")
  text = ""
  i = 0
  p = Paru::PandocFilter::Para.new([])
  dirs.each do |item |
		p.inner_markdown += item
		end
   document.append(p)
  end
