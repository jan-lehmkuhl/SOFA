#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Sebastian Tueck, Jan Lehmkuhl                               #
# Topic:       Project builder                                             #
#--------------------------------------------------------------------------#

# import librarys
import json
import os
import sys
import argparse
import fnmatch

# add paths
file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, file_path ) 
sys.path.insert(1, os.path.realpath( file_path +'/../openFoam/python' ) ) 

# import from sofa
from fileHandling import createDirSafely
from fileHandling import copyFileSafely
from jsonHandling import loadJson
from fileHandling import hasRepositoryStagedFiles
from folderHandling import findParentFolder
from testing.isThisATest import isThisAnInternalSofaTest

from study import Study 

from aspect import Aspect       # only for old init
from fileHandling import findFile       # only for old init

from aspect import readFoamStructure

from case import cfdAspectSelector
from case import Case


def exitIfRepositoryIsNotClean(): 
    if hasRepositoryStagedFiles(): 
        raise SystemExit(  "\nERROR: this git repository has already staged files  \
                            \n       please unstage or commit them and try again\n")



###############################################################################
# MAIN PROGRAMM
###############################################################################

# read arguments and options from command line
parser = argparse.ArgumentParser(description='input for sofa-tasks.py')
parser.add_argument( 'entryPoint',      help="chose the task for this python script" ) 
parser.add_argument( '--verbose', '-v', action="store_true", dest="verbose", default=False )
parser.add_argument( '--no-absolute-path', action="store_true", dest="noAbsolutePathOutput", default=False )
parser.add_argument( '--studyName',         nargs='?', const=1, type=str )
parser.add_argument( '--studyStructFolder', nargs='?', const=1, type=str )
# store all parsed arguments to args
args = parser.parse_args()

if isThisAnInternalSofaTest():
    args.verbose = True
    args.noAbsolutePathOutput = True
if args.verbose :   print("starting sofa-tasks.py in verbose mode" )
if args.verbose :   print("    with passed entryPoint:  " + args.entryPoint  )
if not args.noAbsolutePathOutput:
    if args.verbose :   print("    in folder (os.getcwd):   " + os.getcwd() )
    if args.verbose :   print("    with sofa-tasks.py in:   " + file_path )
    if args.verbose :   print("    adding also path for:    " + os.path.realpath( file_path +'/../openFoam/python' ) )

foamStructure   = readFoamStructure( verbose=args.verbose )

if args.entryPoint == "initStudy":
    # create new study depending on available arguments
    exitIfRepositoryIsNotClean()
    if args.studyStructFolder and args.studyName:
        newStudy = Study( studyName=args.studyName, studyStructFolder=args.studyStructFolder, verbose=args.verbose )
    elif args.studyName : 
        newStudy = Study( studyName=args.studyName, verbose=args.verbose )
    elif args.studyStructFolder:
        newStudy = Study( studyStructFolder=args.studyStructFolder, verbose=args.verbose )
    else :
        newStudy = Study( verbose=args.verbose )

# delete
elif args.entryPoint == "initFoam":
    projectStruct = loadJson( findParentFolder('sofa.project.json') +'/' +'sofa.project.json', verbose=args.verbose )
    for studyFolder in projectStruct['foamFolders']:
        if not os.path.exists(findParentFolder('sofa.project.json') +'/' +studyFolder):
            print("creating study:     " +studyFolder )
            for element in foamStructure:
                newAspect = Aspect(element, os.path.join(findParentFolder('sofa.project.json'), studyFolder) )
                newAspect.create()
            copyFileSafely( os.path.realpath( findFile( "study-documentation.md", "tools" ) ) 
                          , os.path.join( findParentFolder("sofa.project.json"), +studyFolder, "/README-study.md" ) )
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

# new case from aspect level
elif args.entryPoint == "newCase":
    exitIfRepositoryIsNotClean()
    newCaseXXX = Case( verbose=args.verbose )
    newCaseXXX.create( createNew=True )

# (re-)initialize case on case level and copies sofa files again
elif args.entryPoint == "initCase":
    exitIfRepositoryIsNotClean()
    initCaseXXX = Case( verbose=args.verbose )
    initCaseXXX.create()

elif args.entryPoint == "upstreamLinks":
    print("*** update Upstream-Links in ", os.path.basename(os.getcwd()), " ***" )
    thisCase = Case( verbose=args.verbose )
    thisCase.create()
    thisCase.createUpstreamAspectLinks()

elif args.entryPoint == "clone":
    exitIfRepositoryIsNotClean()
    currentCase = Case( verbose=args.verbose )
    currentCase.clone()

# todo
elif args.entryPoint == "overview":
    createDirSafely("doc")
    files = sorted(os.listdir("doc"))
    for fileName in files:
        if fnmatch.fnmatch(fileName, "*verview*.Rmd"):
            os.system('R -e "rmarkdown::render(\'doc/' + fileName + '\')"')
            break
    else:
        print("Found no RMarkdown file for OverviewReports")

elif args.entryPoint == "updateAllReports":
    while True:
        print("Run all reports after updating report files? (y/n)")
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
        files = sorted(os.listdir("doc"))
        for fileName in files:
            if fnmatch.fnmatch(fileName, "*verview*.Rmd"):
                os.system('R -e "rmarkdown::render(\'doc/' + fileName + '\')"')
                break
        else:
            print("Found no RMarkdown file for OverviewReports")

elif args.entryPoint == "updateSofaFiles":
    pass

else:
    raise SystemExit("ERROR no sofa-task defined")

if args.verbose:     print("\n*** finished sofa-tasks.py *** \n")
