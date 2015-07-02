#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Description: CLI program to convert xml to a python literal form.
# Copyright: Copyright (c) 2011 Seibo Software Studios
# Date: $Date: $
# Revision: $Revision: $
# LastChangedBy: $LastChangedBy: $
# HeadURL: $HeadURL: $


def py_element (ele,  strict=False):
    """Process recursively the individual element 'ele' converting it into a python dictionary.
    Each subnode is converted in an item in this dictionary. 
    There are to modes of converting xml into python:
    Strict -- 
    Evrything is converted into dictionaries, each xml tag is converted in a key and elements in items of a  list.
    <a ... >
       <b ...>B1</b>
       <b ...>B2</b>
       <c ...>
            C1
            <d ...>
                D1
            </d>
            C2
       </c>
    </a>
    is converted into:
    {
    'a':[{ '__': 0, ...,
            'b': [{ '__': 0, ..., 
                    '_': [{'__': 0, '_': 'B1'}]}, 
                { '__': 1, ..., 
                    '_': [{'__': 0, '_': 'B2'}]
            }],
            'c': [{ '__': 2..., 
                    '_': [{'__': 0, '_': 'C1'}, {'__': 2, '_': 'C2'}],
                    'd': [{'__': 1, ...,
                        '_': [{'__': 0, '_': 'D1'}]
                    }]
            }]
    }]
    }
    Relaxed --   
    If multiple subnodes have the same tag, they are converted into al Python list.
    If a key-value pair has the form x:{y:[...]} , it is converted into x: [...], ignoring the middle key y"""
    result = {}
    rc = []
    chs = ele.childNodes
    ordinal = -1
    for ch in chs:
        if ch.nodeType == ch.ELEMENT_NODE:
            key = ch.tagName
            if not strict:
                if key in result:
                    if not isinstance (result [key], list):
                        result [key] = [result [key]]
                    result [key].append (py_element (ch))
                else:
                    result [key] = py_element (ch)
            else:
                if not key in result:
                    result [key] = []
                d = py_element (ch,  strict=True)
                if d:
                    ordinal += 1
                    d ['__'] = ordinal
                    result [key] += [d]
        elif ch.nodeType == ch.ATTRIBUTE_NODE:
            result [ch.name + u"_"] = ch.value
        elif ch.nodeType == ch.TEXT_NODE:
            text = ch.data.strip()
            if text:
                if not strict:
                    rc.append (text)
                else:
                    ordinal += 1
                    if not '_' in result:
                        result ['_'] = []
                    d = {'__': ordinal,  '_': text}
                    result ['_'] += [d]
    if not strict:
        txt =  (''.join (rc)).strip ()
        if txt != '':
            result [u"_"] = txt
    attr_prefix = u"_:"
    attrmap = ele.attributes
    attrs = attrmap.keys()
    for attr in attrs:
        result [attr_prefix + attr] = attrmap [attr].value
    if not strict:
        if len (result) == 1 and "_" in result:
            result = result ["_"]
        elif len (result) == 1 and isinstance (result [result.keys () [0]],  list):
            result = result [result.keys () [0]]
        if attr_prefix + u'xsi:nil' in result and  result [attr_prefix + u'xsi:nil'] == u'true':
            result = None
        if result == {}: result = u''
    return result
    
def py_document (dom_doc, strict=False):
    """Convert xml-dom document into a Python data structure"""
    top_element = dom_doc.documentElement
    result = {}
    if not strict:
        result [top_element.tagName] =  py_element (top_element)
    else:
        d = py_element (top_element,  strict=True)
        d ['__'] = 0
        result [top_element.tagName] =  [d]
        
    return result
    
def ignoring_keys (d,  keys):
    """Navigate recursivelly the object 'd' converting it by ignoring all the occurrencies of each key in the given list 'keys'."""
    if isinstance (d, list):
        result = [ignoring_keys (x,  keys) for x in d]
    elif isinstance (d,  dict):
        result = {}
        ks = d.keys()
        for k in ks:
            if k == 'npl:routes':
                pass
            if not k in keys:
                v = d [k]
                result [k] = ignoring_keys (v,  keys)
    else:
        result = d
    return result
    
def reduced_oel (d,  pairs):
    """Convert dictionaries representing one-element-lists to proper lists with one element
    The argument pairs is a list of two element items. If the pair is ['alist', 'anelement'], 
    each occurrence of the sequence of keys 'alist': {'anelement: xyx} is converted in a oel (one element list): alist: [xyx]"""
    if isinstance (d, list):
        result = [reduced_oel (x,  pairs) for x in d]
    elif isinstance (d,  dict):
        result = {}
        ks = d.keys()
        for k in ks:
            if k in pairs and isinstance (d [k],  dict) and len (d [k]) == 1 and d [k].keys()[0] in pairs [k]:
                k1 = d [k].keys()[0]
                d [k] = [d [k][k1]]
            v = d [k]
            result [k] = reduced_oel (v,  pairs)
    else:
        result = d
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

    parser.add_option("-s", "--strict",
                      action="store_true", default=False,  dest="strict", 
                      help = "Generate python in strict mode")

    parser.add_option("-k", "--ignore_keys", dest="keys",
                      help="Ignore given keys in the output. Eg: -k xlns, npl")

    parser.add_option("-e", "--oel", dest="oel",
                      help="Key combinations represnting one element lists. Eg: -e patients/patient, prices/price")

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
        
    strict = options.strict
    
    ignore_keys = False
    if options.keys:
        ignore_keys = True
        if options.keys [0] == "@":
            fn = options.keys [1:]
            f = file (fn)
            keys = f.readlines()
            f.close()
        else:
            keys = options.keys.split (",")
        keys = [x.strip() for x in keys]

    generate_oel = False
    if options.oel:
        generate_oel = True
        if options.oel [0] == "@":
            fn = options.oel [1:]
            f = file (fn)
            pairs = f.readlines()
            f.close()
        else:
            pairs = options.oel.split (",")
            
        oel_pairs = {}
        for p in pairs:
            p = p.split ("/")
            if len (p) != 2: sys.exit (1)
            p = [x.strip() for x in p]
            if not p[0] in oel_pairs :
                oel_pairs [p[0]] = []
            oel_pairs [p[0]] += [p [1]]

    
    dom_document = xml.parse (input)
    pydata = py_document (dom_document, strict=options.strict)
    if ignore_keys:
        pydata = ignoring_keys (pydata, keys)
        
    if generate_oel:
        pydata = reduced_oel (pydata,  oel_pairs)
        
    pprint.pprint (pydata,  stream=output,  indent=1)
