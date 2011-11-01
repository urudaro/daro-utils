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
    k = options.key
    if isinstance (obj,  dict):
        if k in obj:
            o = obj [k]
            pprint.pprint (o)
        else:
            sys.exit (1)
    else:
        i = int (k)
        o = obj [i]
        pprint.pprint (o)
else:
    pprint.pprint (obj)
    
    