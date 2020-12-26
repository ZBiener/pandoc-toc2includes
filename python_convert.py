#!/usr/bin/env python
# 

import sys
import os
import argparse
import re
from pathlib import Path


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
    return[os.path.abspath(args.filename), args.base_directory]


def load_file_contents_to_memory(filename):
    with open(filename, 'r') as f:
        input_file_content = f.readlines()
    return input_file_content

def separate_pandoc_section(input_file_content):
    p = re.compile('other available files', re.IGNORECASE)
    split_position = [index for index,line in enumerate(input_file_content) if p.search(line)]
    input_toc_section = input_file_content[:split_position[0]]
    return(input_toc_section)

def find_md_files_in_directory_tree(base_directory):
    available_markdown_files = list(Path(base_directory).rglob('*.md'))
    return available_markdown_files


def regexp_for_filename_match():
    p = re.compile(r'^\s*(?P<plusminus>[\+-])\s*(?P<filename>.*\.md)\s*$')
    return p


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

def process_headings(toc_section_with_includes):
    toc_section_with_includes_and_headings = []
    for line in toc_section_with_includes:
        line = re.sub("\s{6}\+(.*)", r"####\1\n", line)
        line = re.sub("\s{4}\+(.*)", r"###\1\n", line)
        line = re.sub("\s{2}\+(.*)", r"##\1\n", line)
        line = re.sub("\s{0}\+(.*)", r"#\1\n", line)
        toc_section_with_includes_and_headings.append(line)
    return toc_section_with_includes_and_headings   

def array_difference(available_md_files, toc_files):
    available_files_not_in_toc = [x for x in available_md_files  if x not in set(toc_files)]
    return available_files_not_in_toc

def process_input_file(filename, base_directory):
    input_file_content = load_file_contents_to_memory(filename)
    input_toc_section = separate_pandoc_section(input_file_content)
    toc_files, toc_section_with_includes  = process_file_includes(input_toc_section, base_directory)
    toc_section_with_includes_and_headings = process_headings(toc_section_with_includes)
    toc_files.append(filename)
    return (input_toc_section, toc_files, toc_section_with_includes_and_headings)


def find_remaining_files(toc_files, base_directory):
    available_md_files = find_md_files_in_directory_tree(base_directory)
    remaining_files_not_in_toc = array_difference(available_md_files, toc_files)
    return remaining_files_not_in_toc

def output_to_pandoc(new_toc_section):
    pandoc_output = ''.join(new_toc_section)
    print(pandoc_output)

def output_to_file(filename, input_toc_section, remaining_files):
    file_output = ''.join(input_toc_section) + '::: {OTHER AVAILABLE FILES} :::\n\n' + ''.join('\t-{}\n'.format(k) for k in remaining_files)
    with open(filename, 'w') as f:
       f.write(file_output)


def main():
    [filename, base_directory] = process_command_arguments()
    input_toc_section, toc_files, new_toc_section = process_input_file(filename, base_directory)
    remaining_files = find_remaining_files(toc_files, base_directory)
    output_to_pandoc(new_toc_section)
    output_to_file(filename, input_toc_section, remaining_files)


if __name__ == "__main__":
    main()