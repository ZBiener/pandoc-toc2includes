#! /usr/bin/env python

# Reads directory structure, outputs as markdown tree.

import os
import re
if os.name == 'nt':
    import win32api, win32con

dirname = "Draft"
mainfile = "main.md"
fname = dirname + "/" + mainfile


def load(fname):
    with open(fname) as f:
        content = f.readlines()
        content = [x.strip() for x in content] 

def readDirectory(dirname):
    exclude_list = []
    for dirpath, dirs, files in os.walk(dirname, topdown=True):
        if re.match('^((?!\/\.).)*$', dirpath) is not None:                         #is the directory or its parents hidden?
            path = dirpath.split('/')                                               ## TODO: this will be sensitive to absolute paths. Revise
            print("\n" + (len(path)-1)*'#',os.path.basename(dirpath),"\n")
            for f in files:
                if f.endswith(".md") and not f.startswith('.') and ((dirpath + "/" + f) != fname):
                    print("$include", dirpath + "/" + f, "\n")


def main():
    load(fname)
    readDirectory(dirname)


if __name__ == '__main__':
    main()