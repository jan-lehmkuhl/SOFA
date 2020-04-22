#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Jan Lehmkuhl                                                #
# Topic:       do SOFA-project stuff                                       #
#--------------------------------------------------------------------------#


# import libraries
# -------------------------------------------------------------------
# import librarys
# import json
import os
# import sys
# import shutil
# import fnmatch
# import subprocess
# import argparse


# add additional path for import
# -------------------------------------------------------------------
# sys.path.insert(1, './tools/framework/openFoam/python') 


# load functions
# -------------------------------------------------------------------
# from fileHandling import createDirSafely



def findParentFolder( containingFile, startFolder=os.getcwd() ):
    wd = startFolder
    subdirs = os.listdir(os.getcwd())
    i = 0
    while i < 4:
        if containingFile in subdirs:
            return wd
        else:
            wd = os.path.join(wd, os.path.pardir)
            wd = os.path.abspath( wd )
            subdirs = os.listdir(wd)
            i += 1
    else:
        print("Could not find anything")
        sys.exit(0)

