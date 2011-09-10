#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Description: CLI program to convert xml to a python literal form.
# Copyright: Copyright (c) 2011 Seibo Software Studios
# Date: $Date: $
# Revision: $Revision: $
# LastChangedBy: $LastChangedBy: $
# HeadURL: $HeadURL: $

def py_element (ele):
    """Process recursively the individual element 'ele' converting it into a python dictionary.
    Each subnode is converted in a item in this dictionary. 
    If many subnodes has the same tag, they are converted into al Python list.
    If a key, value pair has the form x:{y:[...]} , it is converted into x: [...], ignoring the middle key y"""
    result = {}
    rc = []
    chs = ele.childNodes
    for ch in chs:
        if ch.nodeType == ch.ELEMENT_NODE:
            key = ch.tagName
            if key in result:
                if not isinstance (result [key], list):
                    result [key] = [result [key]]
                result [key].append (py_element (ch))
            else:
                result [key] = py_element (ch)
        elif ch.nodeType == ch.ATTRIBUTE_NODE:
            result [ch.name + u"_"] = ch.value
        elif ch.nodeType == ch.TEXT_NODE:
            rc.append (ch.data)
    txt =  (''.join (rc)).strip ()
    if txt != '':
        result [u"_"] = txt
    s = u""
    if len (result) != 0:
        s = u"_:"
    attrmap = ele.attributes
    attrs = attrmap.keys()
    for attr in attrs:
        result [s + attr] = attrmap [attr].value
    if len (result) == 1 and "_" in result:
        result = result ["_"]
    elif len (result) == 1 and isinstance (result [result.keys () [0]],  list):
        result = result [result.keys () [0]]
    if s + u'xsi:nil' in result and  result [s + u'xsi:nil'] == u'true':
        result = None
    return result
    
def py_document (dom_doc):
    """Convert xml-dom document into a Python data structure"""
    top_element = dom_doc.documentElement
    result = {}
    result [top_element.tagName] =  py_element (top_element)
    return result
    



if __name__ == '__main__':
    import sys,  os,  pprint
    import optparse

    import xml.dom.minidom as xml

    usage = "usage: %prog [options] arg"
    parser = optparse.OptionParser(usage)

    parser.add_option("-i", "--input", dest="infn",
                      help="Path of the input file other than stdin")

    parser.add_option("-o", "--output", dest="outfn",
                      help="Path of the output file other than stdout")

    parser.add_option("-t", "--indent", dest="itab",
                      help="Indent size")

    (options, args) = parser.parse_args()

    if options.infn:
        input = file (options.infn)
    else:
        input = sys.stdin

    if options.outfn:
        output = file (options.outfn,  "w+")
    else:
        output = sys.stdout
        
    if options.itab:
        itab = int (options.itab)
    else:
        itab = 1

    
    dom_document = xml.parse (input)
    pydata = py_document (dom_document)
    pprint.pprint (pydata,  stream=output,  indent=1)
