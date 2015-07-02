#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Description: CLI program to evaluate and extract python structures.
# Copyright: Copyright (c) 2011 Seibo Software Studios
# Date: $Date: $
# Revision: $Revision: $
# LastChangedBy: $LastChangedBy: $
# HeadURL: $HeadURL: $

import sys
import ast
#import os
import pprint


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

import argparse
parser = argparse.ArgumentParser(description="Retrieve data from Python structured data")
parser.add_argument('-k','--key', help='"Value associated to a key in a dictionary or an index in a list"')
parser.add_argument('-i','--infn', help="Path of the input file other than stdin")
parser.add_argument('-t','--ptype', help="Check if the object is a dict or a list")
parser.add_argument('-r','--rep', action="store_true",  default=False,  help="Report keys, type and len of object")
parser.add_argument('-l','--ls', action="store_true",  default=False,  help="List keys in separated rows")
parser.add_argument('-e','--regexp',  help="Filter dictionary matching regular expression")
parser.add_argument('-v','--verbose', action="store_true",  default=False)

#parser.add_argument('command', choices=['test', 'lookup', 'search'],  help='Perform command. valid values: test, lookup, search.')
global verbose_output

args = parser.parse_args ()
verbose_output = args.verbose

if args.infn:
    f = file (args.infn)
    input = f.read()
    f.close()
else:
    input = sys.stdin.read()

obj = ast.literal_eval (input)

if args.rep:
    l = len (obj)
    t = repr (type(obj))
    if isinstance (obj, dict):
        ks = repr (obj.keys())
    else:
        ks = None
    pprint.pprint ({'len': l, 'type': t, 'keys': ks})
    sys.exit(0)

if args.ls:
    result = []
    if isinstance (obj,  dict):
        result = [x.encode ("utf8") for x in  obj.keys()]
        result.sort()
    print "\n".join (result)
    sys.exit (0)

if args.regexp:
    if isinstance (obj,  dict):
        import re
        rexp = re.compile (args.regexp)
        ks = filter (lambda x: rexp.search (x),  obj.keys())
        result = pprint.pformat (dict ([(k, obj [k]) for k in ks]))
        print result
        sys.exit (0)
    else:
        sys.exit (1)

if args.ptype:
    t = ast.literal_eval (args.ptype)
    if  isinstance (obj,  t):
        sys.exit (0)
    else:
        sys.exit (1)
elif  args.key:
    ks = args.key
    ks = ks.split ("/")
    o = obj
    last_k = ""
    result = None
    for k in ks:
        k = last_k + k
        last_o = o
        o = addressed_obj  (o, k)
        if o:
            result = o
            last_k = ""
        else:
            result = None
            o = last_o
            last_k = k + "/"
    pprint.pprint (result)
else:
    pprint.pprint (obj)
