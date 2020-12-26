#!/usr/local/env python

"""
Add table of contents at the beginning;
uses optional metadata value 'toc-depth'
"""

from panflute import *
import sys
import os

def prepare(doc):
    doc.newHeaders = list()
    blockcount = 0
    

   

# def action(elem, doc):
#    if type(elem) == BulletList and type(elem.parent) == ListItem:
#        return OrderedList(*elem.content)
#        #print(stringify(elem))
#    if type(elem) != BulletList:
#        pass
        
# converts all list item to headings.
# def convertListItemToHeadings(elem, doc):
#    i=1
#    if (type(elem) == ListItem):
#        #debug(elem)
#        for Inline in elem.content:
#            if type(Inline) == BulletList:
#                i += 1
#                debug(Inline)
#                convertListItemToHeadings(Inline, doc) 
#                # narrow to, e.g., Plain(Str(3rd) Space Str(level))
#                # removes the nested bulletlists when they are listitems themselves
#                # and just skips to their own listitems.
#                #for i in range(1, 9):
#                    #debug(type(Inline.ancestor(i)))
#                    #if (type(Inline.ancestor(i)) == type(doc)):
#                i -= 1
#            else:
#                newHead = Header(*Inline.content, level=i, identifier=stringify(Inline))
#                doc.newHeaders.insert(0, newHead)
#            
def convertInlineBulletItem(Inline):
       newHead = Header(*Inline.content, level=2, identifier=stringify(Inline))
       debug("newHEad: ", *Inline.content)
       listgroup.append(newHead)
        
    
# def action(elem, doc):
#     if type(elem) == ListItem:
#         debug("elem: ", elem)
#         for Inline in elem.content:
#             if type(Inline) != BulletList:  
#                 action(Inline, doc) 
#                 newHead = Header(*Inline.content, level=2, identifier=stringify(Inline))
#                 debug("newHEad: ", *Inline.content)
#                 doc.newHeaders.append(newHead)



def action(elem, doc):  
    level = 1
    if isinstance(elem, BulletList) and isinstance(elem.ancestor(level), Doc):
        drillIntoLists(elem,doc,level)

def drillIntoLists(elem, doc, level):
    for Inline in elem.content:
            for i in Inline.content:
                if type(i) != BulletList:
                    #debug(level, *i.content)
                    newHead = Header(*i.content, level=level, identifier=stringify(Inline))
                    #debug("newHEad: ", newHead)
                    doc.newHeaders.append(newHead)
                else:
                    level += 1
                    drillIntoLists(i, doc, level)
                    level -= 1

# def action(elem, doc):
#     group = []
#     x = 0
#     if type(elem) == ListItem:
#         for Inline in elem.content:
#             if type(Inline) != BulletList: 
#                 debug(Inline)
#                 for i in range(1, 9):
#                     if type(Inline.ancestor(i)) == Doc:
#                         x = i
#                         debug((i-1)/2, "ances: ", Inline.ancestor(i))

              #debug(elem.ancestor(i))
            #     convertListItemToHeadings(elem,doc)
            #    break

def notify(elem, doc):
    debug(elem)

#def action(elem, doc):
#    if (type(elem) == BulletList):
#        for listitem in elem.content: 
#            if type(listitem) == ListItem:
#                #debug(listitem.content)
#                for Inline in listitem.content:
#                    if type(Inline) != BulletList:   
#                        newHead = Header(*Inline.content, level=2, identifier=stringify(Inline))
#                        doc.newHeaders.insert(0, newHead)
#             

def finalize(doc):
    for i in reversed(doc.newHeaders):
        doc.content.insert(0, i)
    del doc.newHeaders


def main(doc=None):
    return run_filter(action, prepare=prepare, finalize=finalize, doc=doc) 


if __name__ == '__main__':
    main()