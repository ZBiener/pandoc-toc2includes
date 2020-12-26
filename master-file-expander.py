#!/usr/bin/env python
# 

import sys
import os
import argparse
import re
from pathlib import Path

global base_directory, input_file

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
    global base_directory, input_file
    base_directory = args.base_directory
    input_file = os.path.abspath(args.filename)

def load_file(input_file):
    with open(input_file, 'r') as f:
        input_file_content = f.readlines()
    pattern = re.compile('other available files', re.IGNORECASE)
    split_position = [index for index,line in enumerate(input_file_content) if pattern.search(line)]
    input_toc_section = input_file_content[:split_position[0]]
    return(input_toc_section)

def find_md_files_in_directory_tree(base_directory):
    available_markdown_files = list(Path(base_directory).rglob('*.md'))
    return available_markdown_files
  
def normalize_path(path):
    if os.path.isabs(path):
        return Path(os.path.normpath(path))
    else: 
        return Path(os.path.normpath(os.path.join(base_directory, path)))


def match_filename_pattern(line):
    pattern = re.compile(r'^\s*(?P<plusminus>[\+-])\s*(?P<filename>.*\.md)\s*$')
    return pattern.search(line)

def format_include_statement(line):
    match = match_filename_pattern(line)
    if match:
        filepath = normalize_path(match.group('filename'))
        if match.group('plusminus') == '+' and os.path.exists(filepath): 
            include_statement = f'{{include="{filepath}"}}\n\n'
            return include_statement
        elif match.group('plusminus') == '-' and os.path.exists(filepath): 
            return ''
        elif not os.path.exists(filepath):
            return "Problem finding file: " + line
    else:
        return line

def find_toc_files(line):
    match = match_filename_pattern(line)
    if match:
        return normalize_path(match.group('filename')) 

def process_headings(line):
    line = re.sub("\s{6}\+(.*)", r"####\1\n", line)
    line = re.sub("\s{4}\+(.*)", r"###\1\n", line)
    line = re.sub("\s{2}\+(.*)", r"##\1\n", line)
    line = re.sub("\s{0}\+(.*)", r"#\1\n", line)
    return line 

def array_difference(available_md_files, toc_files):
    available_files_not_in_toc = [x for x in available_md_files  if x not in set(toc_files)]
    return available_files_not_in_toc

def validate_input_toc(line):
    match = match_filename_pattern(line)
    if match and not os.path.exists(normalize_path(match.group('filename'))):
        return "Problem finding file :" + line
    else:
        return line 


def process_input_file(input_file):
    input_toc_section = load_file(input_file)
    toc_files = [find_toc_files(line) for line in input_toc_section]
    toc_section = [format_include_statement(line) for line in input_toc_section]
    toc_section = [process_headings(line) for line in toc_section]
    input_toc_section = [validate_input_toc(line) for line in input_toc_section]
    return (input_toc_section, toc_files, toc_section)


def find_remaining_files(toc_files):
    toc_files.append(normalize_path(input_file))
    available_md_files = find_md_files_in_directory_tree(base_directory)
    remaining_files_not_in_toc = array_difference(available_md_files, toc_files)
    remaining_files_not_in_toc = [Path(os.path.relpath(filename, base_directory)) for filename in remaining_files_not_in_toc]
    return remaining_files_not_in_toc

def output_to_pandoc(new_toc_section):
    pandoc_output = ''.join(new_toc_section)
    print(pandoc_output)

def output_to_file(input_file, input_toc_section, remaining_files):
    file_output = ''.join(input_toc_section) + '::: {OTHER AVAILABLE FILES} :::\n\n' + ''.join('\t\t\t+ {}\n'.format(k) for k in remaining_files)
    with open(input_file, 'w') as f:
       f.write(file_output)


def main():
    process_command_arguments()
    input_toc_section, toc_files, new_toc_section = process_input_file(input_file)
    remaining_files = find_remaining_files(toc_files)
    output_to_pandoc(new_toc_section)
    output_to_file(input_file, input_toc_section, remaining_files)


if __name__ == "__main__":
    main()