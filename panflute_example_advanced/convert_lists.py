"""
Convert all ordered lists into bullet lists
"""

import panflute as pf


def action(elem, doc):
    if isinstance(elem, pf.BulletList)
        return pf.OrderedList(*elem.content)


def main(doc=None):
    return pf.run_filter(action, doc=doc) 


if __name__ == '__main__':
    main()
