
# Basic comparison:

+ Read outline in markdown format
+ Read files and folder directories and subdirectories
+ Compare the directory structure with the outline
+ Add any files to the outline that aren't already there
+ Add heading for any folders, 
+ main yaml should have all metadata for the project.

# Outline view:

## Compilation Settings$$  $$

- [ ] [Overview](#overview)
- [x] [Method and Goals](#method-and-goals)
- [ ] [Assignments](#assignments)
  - [ ] [Reading Outline and Presentation](#reading-outline-and-presentation)
  - [x] [Meeting Scribe](#meeting-scribe)
  - [ ] [Weekly Reading Responses](#weekly-reading-responses)
  - [ ] [Meeting Observer](#meeting-observer)
  - [ ] [Term Paper](#term-paper)
- [ ] [Schedule](#schedule)

## New/Unused documents

- File 1
- Dir/File 2
- Dir2/File 3

The outline view parses the document to determine:
1. Heading structure
2. Whether checked or unchecked



## What is the output?

Yet another file? That seems gratuitous.
It should just run the pandoc command.
This means that it should be a filter. But it can't, since it can only act on files that are already inputted to pandoc.
So it needs to be a wrapper command. 

# What can be done with filters?
Reading the file and parsing contents.


