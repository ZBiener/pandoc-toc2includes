#!/usr/bin/env python
# 

import sys
import os
import argparse
import re
from pathlib import Path

def load_file_contents_to_memory(filename):
    with open(filename, 'r') as f:
        input_file_content = f.readlines()
    return input_file_content

# def func(line, p, base_directory):
#     return p.sub(r"{{include='{}'\n\n".format(Path(os.path.join(base_directory,'\\g<filenamep>'))), line)

# works: [p.sub(r"{{include='{}'\n\n".format(Path(os.path.join(base_directory,'\\g<filenamep>'))), line) if (p.search(line) is not None) else line for line in input_file_content]

def filterPick(list,p):
    return [m.group('filename') for l in list for m in [p.search(l)] if (m and m.group('plusminus') == '+')]



def main():
    input_file_content = load_file_contents_to_memory('Draft/main.md')
    p = re.compile(r'^\s*(?P<plusminus>[\+-])\s*(?P<filename>.*\.md)\s*$')
    x = filterPick(input_file_content,p)
    print(x)


if __name__ == "__main__":
    main()


    def process_file_includes(input_toc_section, base_directory):
    toc_files = []
    toc_section_with_includes = []
    p = regexp_for_filename_match()
    for line in input_toc_section:
        match_a_filename = p.search(line)
        if match_a_filename:
            filename_with_path = Path(os.path.join(base_directory,match_a_filename.group('filename')))
            ## add file to the list of files that are mentioned in the toc, whether included or excluded
            toc_files.append(filename_with_path)
            ## when the original line starts with "+", change to include and add to the toc_section_with_includes
            if (match_a_filename.group('plusminus') == '+'):
                toc_section_with_includes.append(p.sub(rf"{{include='{filename_with_path}'}}\n\n", line))     
            ## when the line starts with "-", do not add
            elif match_a_filename and (match_a_filename.group('plusminus') == '-'):
                continue
            ## if not file is matched, add to the toc_section_with_includes without modification
        else:
            toc_section_with_includes.append(line)
    return toc_files, toc_section_with_includes  