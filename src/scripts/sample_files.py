#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Description: Select N files randomly from a given directory
# Authors: Daniel Rodriguez
# Copyright: Copyright (c) 2012, Seibo Software Studios AB.
# Date: 
# Revision: 
# Head URL: 
# Last changed by: 

import argparse, glob, os, random

parser = argparse.ArgumentParser(description="Select N files randomly from a directory")
parser.add_argument('-d','--directory', help='A particular directory',  default=".")
parser.add_argument('-g','--glob', help='A glob pattern', default="*")
parser.add_argument('N', type=int,  help='Number of selected files', default = 1)

args = parser.parse_args()
pattern = os.path.join (os.path.abspath (args.directory), args.glob)
pathlist = glob.glob (pattern)
filelist = [os.path.basename (pth) for pth in pathlist]

if len (filelist) > args.N:
    selected_files = random.sample (filelist, args.N)
    print repr (selected_files)
