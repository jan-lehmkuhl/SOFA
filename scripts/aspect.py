#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Sebastian Tueck, Jan Lehmkuhl                               #
# Last Change: February 01 2019                                            #
# Topic:       Project builder                                             #
#--------------------------------------------------------------------------#

# import librarys
import json
import os
import sys

sys.path.insert(1, './tools/framework/scripts') 

from fileHandling import createDirSafely
from fileHandling import createSymlinkSavely
from fileHandling import copyFileSafely
from fileHandling import copyFolderSafely
from fileHandling import loadJson
from fileHandling import findFile
from fileHandling import handleStudyStructFile
from fileHandling import handleStudyStructFolder

from folderHandling import findParentFolder

from case import findFile
from case import Case


def readFoamStructure( verbose=False ):
    wd              = findParentFolder( "project.json" )
    projectJsonPath = os.path.join(wd, "project.json" )
    projectJson     = loadJson(projectJsonPath, verbose=verbose )
    return projectJson["foamStructure"]


class Aspect(object):
    # base class to handle all operations related to an aspects

    def __init__(self, aspectType, aspectStructure, studyFolder="./", verbose=False):
        self.className3 = "Aspect"          # only for orientation during debugging
        self.verbose    = verbose
        self.aspectType = aspectType
        self.structure  = aspectStructure   # 
        self.studyRoot  = studyFolder
        self.projectRoot= findParentFolder( "project.json" )

        # define aspect folder (self.path)
        self.path       = os.path.join( studyFolder, self.aspectType )


    def create(self):
        # creates an aspect of self.aspectType at location self.studyRoot
        # according to the entrys in the global dictionary foamStructure
        #
        # Args:
        #
        # Return:
        #   side effects: creates Aspect
        #

        aspectName      = self.aspectType       # renaming from historical reasons 

        # create aspect folder
        createDirSafely( self.path, self.projectRoot )

        # create aspect content
        if 'folders' in self.structure : 
            for thisFolder in self.structure['folders'] : 
                handleStudyStructFolder( self.structure['localpath'], thisFolder, self.path, self.verbose, debugRefPath=self.projectRoot ) 
        if 'files' in self.structure : 
            for thisFile in self.structure['files'] : 
                handleStudyStructFile( self.structure['localpath'], thisFile, self.path, self.verbose, debugRefPath=self.projectRoot ) 

        # call case creation
        newCase001 = Case(  storagePath =   self.path, 
                            aspectType =    self.aspectType, 
                            caseStructure = self.structure['case000'],
                            verbose =       self.verbose
                        )
        newCase001.create()

