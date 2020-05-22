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
from folderHandling import findParentFolder

from case import findFile
from case import cfdAspectSelector


def readFoamStructure():
    wd              = findParentFolder( "project.json" )
    projectJsonPath = os.path.join(wd, "project.json" )
    projectJson     = loadJson(projectJsonPath)
    return projectJson["foamStructure"]


class Aspect(object):
    # base class to handle all operations related to an aspects

    def __init__(self, aspectType, rootFolder="./"):
        self.className = "Aspect"       # only for orientation during debugging
        self.aspectType = aspectType
        self.path = rootFolder

    def create(self):
        # creates an aspect of self.aspectType at location self.path
        # according to the entrys in the global dictionary foamStructure
        #
        # Args:
        #
        # Return:
        #   side effects: creates Aspect
        #

        aspectName      = self.aspectType       
        createDirSafely(os.path.join(self.path, aspectName))
        makefilePath = findFile("Makefile_aspect.mk", "tools")
        if makefilePath:  # if find file fails it returns false
            #copyFileSafely(makefilePath, os.path.join(self.path, aspectName, "Makefile"))
            createSymlinkSavely(    makefilePath,       # aspect Makefile
                                    os.path.join( self.path, aspectName, "Makefile") )
            reportTemplate = loadJson( os.path.join( findParentFolder('project.json'), 'tools/framework/openFoam/dummies/json/', aspectName+'.json') )['buildSettings']['report']
            if self.aspectType == "mesh":
                toolsPath   = os.path.join(findParentFolder('project.json'), "tools") 
                meshOvPath  = findFile("meshOverview.Rmd", toolsPath )
                meshRepPath = findFile("meshReport.Rmd"  , toolsPath )
                createDirSafely(os.path.join(self.path, aspectName, "doc", reportTemplate ))
                if meshOvPath:
                    copyFileSafely(meshRepPath, os.path.join(self.path, aspectName, "doc", reportTemplate, "meshReport.Rmd"))
                    copyFileSafely(meshOvPath,  os.path.join(self.path, aspectName, "doc/meshOverview.Rmd"))
            if self.aspectType == "run":
                createDirSafely(os.path.join(self.path, aspectName, "doc", reportTemplate ))
                runOvPath = findFile("runOverview.Rmd", "tools")
                runRepPath = findFile("runReport.Rmd"  , "tools")
                if runOvPath:
                    copyFileSafely(runRepPath, os.path.join(self.path, aspectName, "doc", reportTemplate, "runReport.Rmd"))
                    copyFileSafely(runOvPath, os.path.join(self.path, aspectName, "doc/runOverview.Rmd"))
            if(    self.aspectType == "mesh" 
                or self.aspectType == "run" ):
                gitignorePath  = findFile(".gitignore_aspect_docs", "tools")
                if gitignorePath:
                    createSymlinkSavely( gitignorePath, 
                                         os.path.join( self.path,  aspectName, "doc/.gitignore"))
            case = cfdAspectSelector(os.path.join(self.path, aspectName))
            case.create()


