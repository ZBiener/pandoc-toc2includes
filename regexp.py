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