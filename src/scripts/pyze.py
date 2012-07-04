#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Description: CLI program to evaluate and extract python structures.
# Copyright: Copyright (c) 2011 Seibo Software Studios
# Date: $Date: $
# Revision: $Revision: $
# LastChangedBy: $LastChangedBy: $
# HeadURL: $HeadURL: $

import sys,  os,  pprint
import optparse

def addressed_obj (obj, k):
    """Subobject addressed by the key 'k'"""
    if isinstance (obj,  dict):
        if k in obj:
            o = obj.get (k)
            return o
    elif k.isdigit and (isinstance (obj, list) or isinstance (obj, tuple)):
        try:
            i = int (k)
            o = obj [i]
        except:
            sys.exit (2)
        return o
    else:
        sys.exit (1)


usage = "usage: %prog [options] arg"
parser = optparse.OptionParser(usage)

parser.add_option("-k", "--key", dest="key",
                  help="Dictionary key or index in a list")

parser.add_option("-i", "--input", dest="infn",
                  help="Path of the input file other than stdin")

parser.add_option("-t", "--type", dest="ptype",
                  help="Test Python type of the evaluated object")

parser.add_option("-r", "--report", dest="rep",
                  help="Report type and keys of the evaluated object")

(options, args) = parser.parse_args()

if options.infn:
    f = file (options.infn)
    input = f.read()
    f.close()
else:
    input = sys.stdin.read()

obj = eval (input)

if options.rep:
    l = len (obj)
    t = repr (type(obj))
    if isinstance (obj, dict):
        ks = repr (obj.keys())
    else:
        ks = None
    pprint.pprint ({'len': l, 'type': t, 'keys': ks})

if options.ptype:
    t = eval (options.ptype)
    if  isinstance (obj,  t):
        sys.exit (0)
    else:
        sys.exit (1)
elif  options.key:
    ks = options.key
    ks = ks.split ("/")
    o = obj
    last_k = ""
    for k in ks:
        k = last_k + k
        last_o = o
        o = addressed_obj  (o, k)
        if o != None:
            last_k = ""
        else:
            o = last_o
            last_k = k + "/"
    pprint.pprint (o)
else:
    pprint.pprint (obj)
    
    
