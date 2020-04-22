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
from folderHandling import findParentFolder



class studyStructure(object):

    def __init__(self, passedStructure="notSet"):
        # search and list possible study structures
        #   1. already used study structures in this project
        #   2. `~/.config/sofa/known-sofa-study-structures.list`
        #   3. tools/framework/sofa-study-structures
        #   4. enter repository with subfolder
        pass

        # read user input of desired studyStructure
        self.url            = "tools/framework/study-structures/openfoam"
        # if new repository
            # store sofa-study-structure URL to `~/.config/sofa/known-sofa-study-structures.list` or `%appdata%\sofa\known-sofa-study-structures.list`
        # import submodule to tools
        self.local          = "tools/framework/study-structures/openfoam"

        # load study structure and assign to self.values
        self.json           = loadJson( self.local +"/sofa-study-structure-root.json" )
        self.files          = self.json['files']
        self.aspects        = self.json['aspects']

        self.name           = self.json['name']     # short name for recognising

        # validate study structure
        pass



def askForStudyName( passedName="notSet"):
        # ask for intendet study-name
        name        = "study1"
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

        self.projectRoot    = findParentFolder( containingFile="project.json" )
        self.studyFolder    = self.projectRoot +"/" +self.name

        self.create( )


    def create(self):
        print( "start creation of:    " +self.name  )
        print( "        with type:    " +self.structure.name )

        # make study folder
        if not os.path.exists( self.studyFolder ):
            os.mkdir( self.studyFolder )
        else:
            print("\n*** StudyFolder already exists")
            print(  "to abort press Ctrl+C to integrate the new study ")
            input("press ENTER to proceed: ")

        # loop all aspects
        for element in self.structure.aspects :
            if verbose: print("run through aspect:  " +element)
        pass 

        # commit new created items
        #   maybe stash before looping and pop now



