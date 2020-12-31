#!/usr/bin/env python
# 

import sys
import os
import argparse
import re
from pathlib import Path

global base_directory, input_filename

def process_command_arguments():
    # Initiate the parser with a description
    # take a filename and a path
    text = 'Convert special outline format into table of contents and check against available files.'
    parser = argparse.ArgumentParser(description=text)
    # Add arguments
    parser.add_argument('filename', type=str, help='the filename to process')
    parser.add_argument('base_directory', metavar='directory', nargs='?', help='optional directory to check for available markdown files, defaults to current directory')
    args = parser.parse_args()
    # if no explicit path is given, use the path of the given filename
    # TODO: add command switch to allow the path to be determined by cwd: os.getcwd()
    if args.base_directory is None:
        args.base_directory = os.path.dirname(os.path.abspath(args.filename))
    global base_directory, input_filename
    base_directory = args.base_directory
    input_filename = os.path.abspath(args.filename)

def load_file(input_filename):
    with open(input_filename, 'r') as f:
        input_file_content = f.readlines()
    pattern = re.compile('other available files', re.IGNORECASE)
    split_position = [index for index,line in enumerate(input_file_content) if pattern.search(line)]
    markdown_input = input_file_content[:split_position[0]]
    return(markdown_input)

def find_md_files_in_directory_tree(base_directory):
    available_markdown_files = list(Path(base_directory).rglob('*.md'))
    return available_markdown_files
  
def normalize_filename(path):
    if os.path.isabs(path):
        return Path(os.path.normpath(path))
    else: 
        return Path(os.path.normpath(os.path.join(base_directory, path)))

def match_and_replace(line):
    # First match filenames - must come before matching of headings
    pattern = re.compile(r'^\s*(?P<plusminus>[\+-])\s*(?P<filename>.*\.md)\s*$')
    match = pattern.search(line)
    if match:
        normalized_filename = normalize_filename(match.group('filename'))
        if os.path.exists(normalized_filename):
            markdown_output = line
            if match.group('plusminus') == '+':
                pandoc_output = f'{{include="{normalized_filename}"}}\n\n'
            elif match.group('plusminus') == '-': 
                pandoc_output = ''
        else:
            markdown_output = pandoc_output = "Problem finding file :" + line
    else:
        normalized_filename = ''
        markdown_output = line
        # then match headings
        pandoc_output = match_and_replace_headings(line)
    return normalized_filename, markdown_output, pandoc_output

def match_and_replace_headings(line):
    # then we match headings
    line = re.sub("\s{6}\+(.*)", r"####\1\n", line)
    line = re.sub("\s{4}\+(.*)", r"###\1\n", line)
    line = re.sub("\s{2}\+(.*)", r"##\1\n", line)
    line = re.sub("\s{0}\+(.*)", r"#\1\n", line)
    return line 

def process_input_file(input_filename):
    markdown_input = load_file(input_filename)
    # List comprehension madness. 
    # For each line, match_and_replace returns a 3-place tuple, the * unpacks the tuple, and zip returns it.
    list_of_files_included_in_TOC, markdown_output, pandoc_output = zip(*(match_and_replace(line) for line in markdown_input ))
    return (list_of_files_included_in_TOC, markdown_output, pandoc_output)


def find_files_that_are_not_included_in_the_toc(list_of_files_included_in_TOC):
    all_md_files_in_directory_tree = find_md_files_in_directory_tree(base_directory)
    list_of_files_in_directory_tree_but_not_TOC = [x for x in all_md_files_in_directory_tree  if x not in set(list_of_files_included_in_TOC)]
    relative_paths_of_files_in_directory_tree_but_not_TOC = [Path(os.path.relpath(filename, base_directory)) for filename in list_of_files_in_directory_tree_but_not_TOC]
    return relative_paths_of_files_in_directory_tree_but_not_TOC

def output_to_pandoc(pandoc_output):
    print(''.join(pandoc_output))

def output_to_file(input_filename, markdown_output, list_of_files_in_directory_tree_but_not_TOC):
    file_output = ''.join(markdown_output) + '::: {OTHER AVAILABLE FILES} :::\n\n' + ''.join('\t\t\t+ {}\n'.format(k) for k in list_of_files_in_directory_tree_but_not_TOC)
    with open(input_filename, 'w') as f:
       f.write(file_output)

def main():
    process_command_arguments()
    list_of_files_included_in_TOC, markdown_output, pandoc_output = process_input_file(input_filename)
    relative_paths_of_files_in_directory_tree_but_not_TOC = find_files_that_are_not_included_in_the_toc(list_of_files_included_in_TOC)
    output_to_pandoc(pandoc_output)
    output_to_file(input_filename, markdown_output, relative_paths_of_files_in_directory_tree_but_not_TOC)


if __name__ == "__main__":
    main()