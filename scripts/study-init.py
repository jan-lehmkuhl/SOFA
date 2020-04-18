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
from fileHandling import loadJson


def prepareStudyStructureInProject():
    # search and list possible study structures
    #   1. already used study structures in this project
    #   2. `~/.config/sofa/known-sofa-study-structures.list`
    #   3. tools/framework/sofa-study-structures
    #   4. enter repository with subfolder

    # read user input of desired studyStructure
    # if new repository
        # store sofa-study-structure URL to `~/.config/sofa/known-sofa-study-structures.list` or `%appdata%\sofa\known-sofa-study-structures.list`
    # import submodule to tools

    return "tools/framework/sofa-study-structures/dummy-structure"


class study(object):

    global verbose

    def __init__(self, studyStructure="notSet", studyName="notSet"):
        if verbose :    print( "start studyStructure __init__ ")

        # prepare study structure
        # =============================================================================
        studyStructureFolder    = prepareStudyStructureInProject( )
        self.studyStructure     = loadJson( studyStructureFolder +"/sofa-study-structure.json" )
        # validate study structure


        # read and validate study folder
        # =============================================================================
        # ask for intendet study-name
        self.studyName          = "AskForName"
        # validate study-name
        #   no doubles
        #   no umlaute
        # check if folder already exists



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



# create study
# =============================================================================

newStudy = study( )
newStudy.create()


print( "END study init" )
