#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Sebastian Tueck, Jan Lehmkuhl                               #
# Topic:       Project builder                                             #
#--------------------------------------------------------------------------#

# import librarys
import json
import os
import sys
# import shutil
# import fnmatch
# import subprocess
import argparse

sys.path.insert(1, './tools/framework/openFoam/python') 

from fileHandling import createDirSafely
# from fileHandling import createSymlinkSavely
from fileHandling import copyFileSafely
# from fileHandling import copyFolderSafely
from fileHandling import loadJson
from folderHandling import findParentFolder

from study import Study 

from aspect import Aspect       # only for old init
from case import findFile       # only for old init

from aspect import readFoamStructure



###############################################################################
# MAIN PROGRAMM
###############################################################################

# read arguments and options from command line
parser = argparse.ArgumentParser(description='input for sofa-tasks.py')
parser.add_argument( 'entryPoint',      help="chose the task for this python script" ) 
parser.add_argument( '--verbose', '-v', action="store_true", dest="verbose", default=False )

entryPoint =    parser.parse_args().entryPoint
verbose =       parser.parse_args().verbose

if verbose :    print("starting in verbose mode" )
if verbose :    print("starting sofa-tasks.py with arg: >" + entryPoint + "< in: " + os.getcwd() )

foamStructure   = readFoamStructure()


if entryPoint == "initFoam":
    newStudy = Study( verbose=verbose )

if entryPoint == "initFoamOld":
    projectStruct = loadJson('project.json')
    for studyFolder in projectStruct['foamFolders']:
        if not os.path.exists(studyFolder):
            print("creating study >" +studyFolder +"< and the interior")
            for element in foamStructure:
                newAspect = Aspect(element, studyFolder)
                newAspect.create()
            copyFileSafely( findFile(    "study-documentation.md", "tools") 
                          , studyFolder+ "/README-study.md" )
            while True:
                print("Commit creation of study %s ? (y/n)" % studyFolder)
                answer = input()
                answer = answer.lower()
                if answer in ["y", "yes"]:
                    os.system('git add .')
                    os.system('git commit -m "[%s] #INIT \'created study %s\'"' % (studyFolder, studyFolder))
                    break
                elif answer in ["n", "no"]:
                    break           
        else:
            print("skipping study >" + studyFolder + " since it already exists")

elif entryPoint == "newCase":
    currentCase = cfdAspectSelector()
    currentCase.create()

elif entryPoint == "initCase":
    currentCase = cfdAspectSelector()
    currentCase.initCase()

elif entryPoint == "symlinks":
    currentCase = cfdAspectSelector()
    currentCase.makeSymlinks()

elif entryPoint == "clone":
    currentCase = cfdAspectSelector()
    currentCase.clone()

elif entryPoint == "clear":
    currentCase = cfdAspectSelector()
    currentCase.clear()

elif entryPoint == "commit":
    currentCase = Case("run")
    currentCase.commitChanges()

elif entryPoint == "overview":
    createDirSafely("doc")
    files = os.listdir("doc")
    for fileName in files:
        if fnmatch.fnmatch(fileName, "*verview*.Rmd"):
            os.system('R -e "rmarkdown::render(\'doc/' + fileName + '\')"')
            break
    else:
        print("Unabel to find RMarkdown file")

elif entryPoint == "updateAllReports":
    while True:
        print("Run reports after updating ? (y/n)")
        answer = input()
        answer = answer.lower()
        if answer in ["y", "yes"]:
            runReports = True
            break
        elif answer in ["n", "no"]:
            runReports = False
            break
    for folder in sorted(os.listdir(".")):
        aspectName = ''.join([i for i in folder if not i.isdigit()])  # remove digits
        if aspectName in foamStructure:
            currentCase = cfdAspectSelector(os.path.join("./", folder))
            currentCase.copyReport(runReports)
    if runReports:
        if not os.path.exists("doc"):
            print("Directory >doc< doesn't exist in: " + os.getcwd() )
            exit(0)
        files = os.listdir("doc")
        for fileName in files:
            if fnmatch.fnmatch(fileName, "*verview*.Rmd"):
                os.system('R -e "rmarkdown::render(\'doc/' + fileName + '\')"')
                break
        else:
            print("Unabel to find RMarkdown file")

elif entryPoint == "updateReport":
    while True:
        print("Run reports after updating ? (y/n)")
        answer = input()
        answer = answer.lower()
        if answer in ["y", "yes"]:
            runReports = True
            break
        elif answer in ["n", "no"]:
            runReports = False
            break
    currentCase = cfdAspectSelector()
    currentCase.copyReport(runReports)

elif entryPoint == "updateJson":
    for folder in sorted(os.listdir(".")):
        aspectName = ''.join([i for i in folder if not i.isdigit()])  # remove digits
        if aspectName in foamStructure:
            print("Updating .json in >%s" %folder)
            currentCase = cfdAspectSelector(os.path.join("./", folder))
            currentCase.updateJson()

elif entryPoint == "test":
    print("Nothing defined")


if verbose:     print("\n*** finished sofa-tasks.py *** \n")
