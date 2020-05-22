#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Jan Lehmkuhl                                                #
# Topic:       Create study epending on specific study structure           #
#--------------------------------------------------------------------------#

# import librarys
import json
import os
import sys

# add additional path for import
file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, file_path )
sys.path.insert(1, './tools/framework/openFoam/python') 

from fileHandling import loadJson
from folderHandling import findParentFolder

from aspect import Aspect


class StudyStructure(object):

    def __init__(self, passedStructure="notSet"):
        # search and list possible study structures
        #   1. already used study structures in this project
        #   2. `~/.config/sofa/known-sofa-study-structures.list`
        #   3. tools/framework/sofa-study-structures
        #   4. enter repository with subfolder
        pass

        # read user input of desired StudyStructure
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


def askForStudyName( defaultName ):
    name = str(input( "\nplease insert the desired study name [" +defaultName +"]: " ))
    if name == "":
        name        = defaultName
    # TODO if validateFolderName( name ):   print("proceed")
    return name 


def validateFolderName(name):
        # validate study-name
        #   no doubles
        #   no umlaute
        return True


class Study(object):

    global verbose

    def __init__(self, passedStructure="notSet", studyName2="notSet", verbose=False):
        if verbose :    print( "start StudyStructure __init__ ")

        self.structure      = StudyStructure( )
        self.name           = askForStudyName( "study1" )

        self.projectRoot    = findParentFolder( containingFile="project.json" )
        self.studyFolder    = self.projectRoot +"/" +self.name

        self.create( verbose )


    def create(self, verbose):
        print("\nstart creation of:         " +self.name  )
        print(  "      with type:           " +self.structure.name )

        # make study folder
        if not os.path.exists( self.studyFolder ):
            print(  "creating study folder:     " +self.studyFolder )
            os.mkdir( self.studyFolder )
        else:
            print("\n*** StudyFolder already exists")
            # input(  "    to abort press Ctrl+C to integrate the new study, press ENTER to proceed: ")

        # loop all aspects
        for element in self.structure.aspects :
            if verbose :    print("run through aspect:  \t" +element)
            newAspect = Aspect(element, self.studyFolder)
            newAspect.create()

        # commit new created items
        #   maybe stash before looping and pop now



