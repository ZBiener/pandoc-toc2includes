#!/usr/bin/env python
# 

from panflute import *


def prepare(doc):
    pass


def action(elem, doc):
    if isinstance(elem, Header):
        elem.level = 1


def finalize(doc):
    pass


def main(doc=None):
    return run_filter(action,
                         prepare=prepare,
                         finalize=finalize,
                         doc=doc) 


if __name__ == '__main__':
    main()