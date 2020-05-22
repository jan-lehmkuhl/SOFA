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
from folderHandling import findChildFolders

from aspect import Aspect


class StudyStructure(object):

    def __init__(self, studyStructFolder, verbose ):

        self.local      = studyStructFolder     # for first try 

        while True: 
            if os.path.exists( self.local +"/sofa-study-structure-root.json"): 
                self.json           = loadJson( self.local +"/sofa-study-structure-root.json" )
                # load study structure and assign to self.values
                self.files          = self.json['files']
                self.aspects        = self.json['aspects']
                self.name           = self.json['name']     # short name for recognising

                # TODO validate study structure
                break
            if self.local != "": 
                print("\nWARNING sofa-study-structure-root.json dont exists in:  " +self.local +"\n")

            # search and list possible local study structures
            sofaStructList      = ['INSERT url to import a new repository to tools']
            sofaStructList.extend( findChildFolders( "sofa-study-structure-root.json", startFolder=os.getcwd()+"/tools" ) )
            # TODO read known structures from `~/.config/sofa/known-sofa-study-structures.yaml`
            sofaStructList.append( studyStructFolder )  # add passed value for retry

            print("\npossible sofa study structures: ")
            for iStruct in range( len(sofaStructList) ):
                print( "idx " +str(iStruct) +"\t" +sofaStructList[iStruct]  ) 

            # read user input of desired StudyStructure
            idxChoosenStruct = int( input("\nchoose study struct by number and press enter: ") )
            self.local          = sofaStructList[idxChoosenStruct]

            if idxChoosenStruct == 0 :
                # TODO 
                self.url            = str(input("insert url used for 'git clone xxx': "))
                # import submodule to tools
                # store sofa-study-structure URL to `~/.config/sofa/known-sofa-study-structures.list` or `%appdata%\sofa\known-sofa-study-structures.list`

        if verbose:     print(  "loaded study struct")



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

    def __init__(self, studyFolder="", studyStructFolder="", verbose=False):
        if verbose :    print( "start StudyStructure __init__ ")

        self.name           = askForStudyName( studyFolder )

        self.projectRoot    = findParentFolder( containingFile="project.json" )
        self.studyFolder    = self.projectRoot +"/" +self.name
        self.structure      = StudyStructure( studyStructFolder, verbose )

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



