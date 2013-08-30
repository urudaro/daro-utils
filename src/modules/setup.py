#!/usr/bin/env python

from distutils.core import setup

setup(name='xpyze',
      version='1.0',
      description='Installation script for my utilities',
      author='Daniel Rodriguez',
      author_email='daro@seibostudios.se',
      url='http://seibostudios.se',
      py_modules=['xpyze', 'simplegit','monitoring'],
      scripts=['pyze', 'xpyze', 'sample_files']
     )

