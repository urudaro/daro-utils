#!/usr/bin/env python

from distutils.core import setup

import os
import shutil

if not os.path.exists('_scripts'):
    os.makedirs('_scripts')

shutil.copyfile('scripts/pyze.py', '_scripts/pyze')
shutil.copyfile('scripts/xpyze.sh', '_scripts/xpyze')
shutil.copyfile('scripts/sample_files.py', '_scripts/sample_files')

setup(name='daro-utils',
      version='1.0',
      description='Installation script for my utilities',
      author='Daniel Rodriguez',
      author_email='daro@seibostudios.se',
      url='http://seibostudios.se',
      package_dir = {"": "modules"},
      packages = ['tracrpc_client'], 
      py_modules=['xpyze', 'simplegit','monitoring'],
      scripts=['_scripts/pyze', '_scripts/xpyze', '_scripts/sample_files']
     )
