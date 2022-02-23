# -*- coding: iso-8859-1 -*-
from distutils.core import setup
import py2exe

setup(windows = [{'script': "app.py"}], zipfile = None)