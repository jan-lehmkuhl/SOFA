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
from fileHandling import handleStudyStructFile
from folderHandling import findParentFolder
from folderHandling import findChildFolders

from aspect import Aspect


class StudyStructure(object):

    def __init__(self, studyStructFolder=None, studyJsonFolder=None, verbose=False ):
        self.className2 = "StudyStructure"
        self.verbose=verbose

        # if provided load specified study struct
        if studyJsonFolder != None: 
            sofaStudyJson       = loadJson( os.path.join( studyJsonFolder, "sofa.study.json" ), verbose=verbose )
            relativePath        = sofaStudyJson['study-structure']
        if studyStructFolder != None: 
            relativePath        = studyStructFolder     # for first try 

        # convert StudyStructure.path to absolute
        if relativePath.startswith("tools"):
            projectRoot     = findParentFolder("project.json")
            self.path       = os.path.join( projectRoot, relativePath )
        elif relativePath.startswith("/"):
            self.path       = relativePath
        else:
            print(  "ERROR: relativePath is not processed right")
            pass  # ERROR TODO

        # try to load study-struct from self.path
        # otherwise a new git-repository can be loaded
        while True: 
            if os.path.exists( os.path.join( self.path, "sofa-study-structure-root.json" ) ): 
                # load study structure root
                self.json           = loadJson( os.path.join( self.path, "sofa-study-structure-root.json" ), verbose=verbose )
                # assign to self.values
                self.name           = self.json['name']     # short name for recognising
                self.files          = self.json['files']    # files to copy in study
                self.aspectList     = self.loadStudyStructAspectList()

                # TODO validate study structure
                break
            if self.path != "": 
                print("\nWARNING sofa-study-structure-root.json dont exists in:  " +self.path +"\n")

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
            self.path           = sofaStructList[idxChoosenStruct]

            if idxChoosenStruct == 0 :
                # TODO 
                self.url            = str(input("insert url used for 'git clone xxx': "))
                # import submodule to tools
                # store sofa-study-structure URL to `~/.config/sofa/known-sofa-study-structures.list` or `%appdata%\sofa\known-sofa-study-structures.list`

        if verbose:     print(  "loaded study struct")


    def loadStudyStructAspectList(self):
        aspectList = findChildFolders("sofa-study-structure-aspect.json", startFolder=self.path, relativeOutput=True )
        struct = dict()
        for aspect in aspectList: 
            localStructAspectPath       = os.path.join( self.path, aspect ) 
            # load aspect root
            struct[aspect]              = loadJson( os.path.join( localStructAspectPath, "sofa-study-structure-aspect.json" ), verbose=self.verbose )
            struct[aspect]['localpath'] = localStructAspectPath
            # TODO put into class for aspect handling 
            # load case000
            struct[aspect]['case000']   = loadJson( os.path.join( localStructAspectPath, "case000", "sofa-study-structure-case.json" ), verbose=self.verbose ) 
            struct[aspect]['case000']['localpath']= os.path.join( localStructAspectPath, "case000" )
        return struct


def askForStudyName( use="", defaultName="newStudy" ):
    if use != "":
        return use

    name = str(input( "\nplease insert the desired study name [" +defaultName +"]: " ))
    if name == "":
        name        = defaultName
    # TODO if validateFolderName( name ): 
    return name 


def validateFolderName(name):
        # validate study-name
        #   no doubles
        #   no umlaute
        return True


class Study(object):

    global verbose

    def __init__(self, studyName=None, studyStructFolder=None, verbose=False):
        if verbose :    print( "start StudyStructure __init__ ")

        self.className1     = "Study"       # only for appearance during debugging
        self.projectRoot    = findParentFolder( containingFile="project.json" )

        # create study folder (self.path)
        self.name           = askForStudyName( use=studyName )
        self.path           = self.projectRoot +"/" +self.name
        self.createFolder( verbose )

        # create study structure
        self.studyStructure = StudyStructure( studyStructFolder=studyStructFolder, verbose=verbose )
        self.createStructure( verbose )


    def createFolder(self, verbose):
        if not os.path.exists( self.path ):
            print(  "creating study folder:     " +self.path )
            os.mkdir( self.path )
        else:
            print("\n*** StudyFolder already exists")
            # input(  "    to abort press Ctrl+C to integrate the new study, press ENTER to proceed: ")
            # TODO mark self.isStudyUpdateMode


    def createStructure(self, verbose):
        print("\nstart structure creation of:       " +self.name  )
        print(  "       with study type:            " +self.studyStructure.name )
        if os.path.exists(self.path):
            print(  "       in folder :                  " +self.path )
        else:
            print("\nERROR: " +self.path +" dont exists")
            sys.exit(1)
        print(" ")

        # loop all study files
        for thisFile in self.studyStructure.files :
            handleStudyStructFile( self.studyStructure.path, thisFile, self.path, verbose ) 
            #TODO write used structure to study.json or it should be stored there in before

        # loop all study aspects
        for element in self.studyStructure.aspectList :
            if verbose :    print("run through aspect:  \t" +element)
            newAspect = Aspect( aspectType =        element, 
                                aspectStructure =   self.studyStructure.aspectList[element], 
                                studyFolder =       self.path, 
                                verbose =           verbose )
            newAspect.create()

        print(  "completed structure creation of:   " +self.name)
        # TODO commit new created items
        #   maybe stash before looping and pop now



