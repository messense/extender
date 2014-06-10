#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

try:
    import pandoc
except ImportError:
    print('Please install pyandoc first, run pip install pyandoc.')
    sys.exit()

pandoc_path = os.popen('which pandoc').read().strip()
if not pandoc_path:
    print('Cannot find pandoc executable file, you should install pandoc.')
    sys.exit()

pandoc.core.PANDOC_PATH = pandoc_path

doc = pandoc.Document()
doc.markdown = open('README.md').read()
f = open('README.rst', 'w+')
f.write(doc.rst)
f.close()
os.system("python setup.py release")
os.remove('README.rst')
