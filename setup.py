#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for deslab
You can install deslab with python setup.py install --user
"""
from distutils.core import setup
from glob import glob
import os
import sys



# Package information

deslab_email = "deslab@ufrj.br"

deslab_description = \
"""DESlab is a scientific computing program 
         for discrete event systems (DES) modeled as automata.
"""

deslab_long_description = \
"""
DESlab
========
    DESlab a scientific computing program written in python
    for the development of algorithms for analysis and synthesis
    of discrete event systems (DES) modeled as automata.
    The main objective of DESlab is to provide a unified tool 
    that integrates automata, graph algorithms, and numerical
    calculations. DESlab also allows the definition of symbolic
    variables of type automaton and incorporates concise
    instructions to manipulate, operate, analyze and visualize
    these variables, with a syntax and an abstraction level close
    to the notation used in DES theory
"""
deslab_keywords = ['Automata', 'Discrete Event Systems', 'Mathematics', 'Graph theory', 'Diagnosis', 'Supervisory Control']

if os.path.exists('MANIFEST'): os.remove('MANIFEST')

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install --user'")
    sys.exit(-1)

if sys.version_info[:2] < (2, 7):
    print("deslab requires Python version 2.7 or later (%d.%d detected)." %
          sys.version_info[:2])
    sys.exit(-1)

if sys.argv[1]== 'install':
    if sys.argv[-1]== 'install':
        print("To install, run 'python setup.py install --user'")
        sys.exit(-1)
    elif sys.argv[-1]== '--user':
        print ("I am installing DESlab")


 
sys.path.insert(0, 'deslab')
sys.path.pop(0)
deslab_packages=["deslab",
                 "deslab.src",
                 "deslab.graphics",
                 "deslab.toolboxes",
                 "deslab.readwrite",
                 ]

deslab_package_data     = {
                           'deslab.graphics': ['output/empty.dat','working/*.py'],
                           'deslab': ['docs/*.pdf'],                          
                           }
     
if __name__ == "__main__":
    
        setup(
        name             = "DESlab",
        version          = "0.0.4",
        maintainer       = "Leonardo Clavijo, Daniel Ramos Garcia, Joao Carlos Basilio, Lilian Kawakami",
        maintainer_email = deslab_email,
        author           = "Leonardo Clavijo, Daniel Ramos Garcia, Joao Carlos Basilio, Lilian Kawakami",
        author_email     = deslab_email,
        description      = deslab_description,
        keywords         = deslab_keywords,
        long_description = deslab_long_description,
        license          = "BSD",
        platforms        = ['windows'],
        url              = "http://www.dee.ufrj.br/lca/",      
        download_url     = "",
        #classifiers      = release.classifiers,
        packages         = deslab_packages,
        #data_files       = data,
        #package_dir      = data_dir,
        package_data     = deslab_package_data,
        scripts=['README.txt'],
        requires=['networkx (>=1.5)']        
      )
