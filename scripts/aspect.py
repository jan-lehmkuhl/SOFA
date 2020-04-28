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
import shutil
import fnmatch
import subprocess
import argparse

sys.path.insert(1, './tools/framework/scripts') 

from fileHandling import createDirSafely
from fileHandling import createSymlinkSavely
from fileHandling import copyFileSafely
from fileHandling import copyFolderSafely
from fileHandling import loadJson
from folderHandling import findParentFolder

from case import findFile
from case import cfdAspectSelector


class Aspect(object):
    # base class to handle all operations related to an aspects

    global foamStructure

    def __init__(self, aspectType, path="./"):
        self.aspectType = aspectType
        self.path = path
        self.name = "Aspect"

    def create(self):
        # creates an aspect of self.aspectType at location self.path
        # according to the entrys in the global dictionary foamStructure
        #
        # Args:
        #
        # Return:
        #   side effects: creates Aspect
        #
        aspectName = foamStructure[self.aspectType]["aspectName"]
        createDirSafely(os.path.join(self.path, aspectName))
        makefilePath = findFile("Makefile_aspect.mk", "tools")
        if makefilePath:  # if find file fails it returns false
            #copyFileSafely(makefilePath, os.path.join(self.path, aspectName, "Makefile"))
            createSymlinkSavely(    makefilePath,       # aspect Makefile
                                    os.path.join( self.path, aspectName, "Makefile") )
            reportTemplate = loadJson( os.path.join('tools/framework/openFoam/dummies/json/', aspectName+'.json') )['buildSettings']['report']
            if self.aspectType == "mesh":
                meshOvPath  = findFile("meshOverview.Rmd", "tools")
                meshRepPath = findFile("meshReport.Rmd"  , "tools")
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


