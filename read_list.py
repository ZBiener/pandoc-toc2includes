#!/usr/local/env python

"""
Add table of contents at the beginning;
uses optional metadata value 'toc-depth'
"""

from panflute import *
import sys
import os

def prepare(doc):
    doc.newHeaders = []


# def action(elem, doc):
#    if type(elem) == BulletList and type(elem.parent) == ListItem:
#        return OrderedList(*elem.content)
#        #print(stringify(elem))
#    if type(elem) != BulletList:
#        pass
        


def action(elem, doc):
    if type(elem) == ListItem:
        for item in elem.content:
            #newHead = "Header("
            ans = []
            for block in item.content:
                #debug(block)
                ans.append(block)
            #debug(ans.t)
            newHead = Header(Inline(ans))
            #debug(newHead)
        #Header(Str(The), Space, Str(Title), level=1, identifier=foo) 
        #debug(elem.content[0].content[0].text)
        #debug(elem.index) ## prints position in list.
        #doc.newHeaders.append(elem)
        #print(stringify(elem))

def finalize(doc):
    doc.content.insert(0, doc.newHead)


def main(doc=None):
    return run_filter(action, prepare=prepare, finalize=finalize, doc=doc) 


if __name__ == '__main__':
    main()