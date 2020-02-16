#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Jan Lehmkuhl                                                #
# Topic:       Create study epending on specific study structure           #
#--------------------------------------------------------------------------#

# import librarys
import json
import os
import sys
import shutil
import fnmatch
import subprocess
import argparse

# add additional path for import
sys.path.insert(1, './tools/framework/openFoam/python') 

# from fileHandling import createDirSafely
# from fileHandling import createSymlinkSavely
# from fileHandling import copyFileSafely
# from fileHandling import copyFolderSafely
# from fileHandling import loadJson




class study(object):

    def __init__(self, studyStructure, studyName):
        self.studyStructure = studyStructure
        self.studyName = studyName
        print( "start __init__ ")


    def create(self):
        # Args:
        #
        # Return:
        print( "start creation of: " +self.studyName)



###############################################################################
# MAIN PROGRAMM
###############################################################################

# enviroment setup
# =============================================================================

# read arguments and options from command line
parser = argparse.ArgumentParser(description='input for openFoam.py')
parser.add_argument( '--verbose', '-v', action="store_true", dest="verbose", default=False )

verbose =       parser.parse_args().verbose

# explain enviroment
if verbose :    print("starting in verbose mode" )
if verbose :    print("starting study-init.py in: " + os.getcwd() )



# get and prepare needed information
# =============================================================================

# search for possible study structures
#   1. `~/.config/sofa/known-sofa-study-structures.list`
#   2. tools
#   3. tools/framework/sofa-study-structures

# choose structure or insert new gitlab link

# read study structure from json and validate structure

# if new store structure 
#   store sofa-study-structure URL to `~/.config/sofa/known-sofa-study-structures.list` or `%appdata%\sofa\known-sofa-study-structures.list`

# ask for intendet study-name

# validate study-name
#   no doubles
#   no umlaute



# create study
# =============================================================================

newStudy = study('dummystruct','emptyStudy')
newStudy.create()


print( "END study init" )
