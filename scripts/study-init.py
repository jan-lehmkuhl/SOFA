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



class studyStructure(object):

    def __init__(self, passedStructure="notSet"):
    # search and list possible study structures
    #   1. already used study structures in this project
    #   2. `~/.config/sofa/known-sofa-study-structures.list`
    #   3. tools/framework/sofa-study-structures
    #   4. enter repository with subfolder
        pass

    # read user input of desired studyStructure
        self.url                = "tools/framework/sofa-study-structures/dummy-structure"
    # if new repository
        # store sofa-study-structure URL to `~/.config/sofa/known-sofa-study-structures.list` or `%appdata%\sofa\known-sofa-study-structures.list`
    # import submodule to tools
        self.local          = "tools/framework/sofa-study-structures/dummy-structure"

        # load study structure
        self.json           = loadJson( self.local +"/sofa-study-structure.json" )
        self.name           = "dummy-structure"     # short name for recognising

        # validate study structure
        pass



def askForStudyName( passedName="notSet"):
        # ask for intendet study-name
        name        = "AskForName"
        if validateFolderName( name):   print("proceed")
        # check if folder already exists
        pass
        return name 


def validateFolderName(name):
        # validate study-name
        #   no doubles
        #   no umlaute
        return True


class study(object):

    global verbose

    def __init__(self, passedStructure="notSet", studyName2="notSet"):
        if verbose :    print( "start studyStructure __init__ ")

        self.structure      = studyStructure( )
        self.name           = askForStudyName( )

        self.create( )


    def create(self):
        print( "start creation of:    " +self.name  )
        print( "        with type:    " +self.structure.name )
        pass 



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


print( "END study init" )
