#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Sebastian Tueck                                             #
# Last Change: February 01 2019                                            #
# Topic:       Solving process                                             #
#--------------------------------------------------------------------------#

import sys
import os
import time
import shutil
import datetime
import hashlib
import pickle
import fnmatch
import json
import subprocess
import openFoam

from fileHandling import createDirSafely
from fileHandling import createSymlinkSavely
from fileHandling import copyFileSafely
from fileHandling import copyFolderSafely
from fileHandling import loadJson

from procHandling import procHandler

def checkFoamVer():
    # retrieves the openFoam version from OS environment
    #
    # Args:
    #
    # Return:
    #   str:     openFoam version
    #
    version = os.environ.get('WM_PROJECT_DIR')
    if version == "/opt/openfoam4":
        return ("4.1")
    elif version == "/opt/openfoam5":
        return ("5")
    elif version == "/opt/openfoam6":
        return ("6")
    elif version == "/opt/openfoam7":
        return ("7")
    elif version == "/opt/openfoam-dev":
        return ("dev")
    elif version == "":
        print("OpenFoam is not sourced")
    else: 
        print("Unknown OpenFoam version")

def md5(filePath):
    # calculates the md5 hash of a file
    #
    # Args:
    #   filePath: path to file
    # Return:
    #   int: md5 hash
    #
    if os.path.isfile(filePath):
        hasher = hashlib.md5()
        with open(filePath, 'rb') as currentFile:
            buffer = currentFile.read()
            hasher.update(buffer)
            return(hasher.hexdigest())
    else: 
        print(">%s< is not a file, can't get md5 sum" %filePath)

def boolChecker(value):
    # takes a str and checkes if it is a bool and then converts 
    #
    # Args:
    #   value:  str: potential bool
    #
    # Return:
    #   bool:
    #
    if value.lower() in ["y", "t", "yes", "true", "on"]:
        return(True)
    elif value.lower() in ["n", "f", "no", "false", "off"]:
        return(False)
    else:
        print("Unknown value >%s< please enter True or False" % value)
        sys.exit(0)

class foamRunner(object):
    # class for openFoam meshing procedures

    def __init__(self):
        # general info
        self.startSolving = datetime.datetime.now()  
        self.foamVer = checkFoamVer()
        self.localHost = os.uname()[1]
        # make sure 0.org exists or is retreived 
        CaseFiles = os.listdir(".")
        if "0.org" in CaseFiles:
            if "0" in CaseFiles:
                shutil.rmtree("0")
            shutil.copytree("0.org", "0")
        elif "0" in CaseFiles:
            shutil.copytree("0", "0.org")
        else:
            print("No boundary files present")
            sys.exit(1)
        # info about the state of case
        self.nProcFolder = self.getNoProcFolder()
        self.fileChangeDict = self.compareFileStates()
        # info from run.json
        self.runJson = loadJson("run.json")
        self.nCores = int(self.runJson["runSettings"]["nCores"])
        self.solver = self.runJson["buildSettings"]["solver"]
        self.runRenumberMesh = boolChecker(self.runJson["runSettings"]["renumberMesh"])
        self.runPotentialFoam = boolChecker(self.runJson["runSettings"]["potentialFoam"])
        self.runSolver = boolChecker(self.runJson["runSettings"]["solver"])
        self.runReconstructPar = boolChecker(self.runJson["runSettings"]["reconstructPar"])
        self.runFoamLog = boolChecker(self.runJson["runSettings"]["foamLog"])
        self.runReport = boolChecker(self.runJson["runSettings"]["report"])
        # decision wether to run decomposePar       
        if self.nCores > 1:
            if self.fileChangeDict["system/decomposeParDict"]:
                self.runDecomposePar = True
            else:
                self.runDecomposePar = False
                self.runRenumberMesh = False
        else:
            self.runDecomposePar = False
            self.runRenumberMesh = False
        # init process handler 
        self.procHandler = procHandler(self.nCores)
        
    ###################################################################
    # general purpose 
    ###################################################################

    def getNoProcFolder(self):
        # count how many processor directories are present 
        #
        # Args:
        #
        # Return:
        #   int:    number of processor directories
        #
        procFolders = [f for f in os.listdir('.') if fnmatch.fnmatch(f, "processor*")]
        if len(procFolders) > 1:
            return(len(procFolders))
        else:
            return(0)

    def loadFileStates(self):
        # load file containing dictionary of filenames and their md5 hashes 
        #
        # Args:
        #
        # Return:
        #   oldFileStates:    dictionary of filenames and their md5 hashes
        #
        if os.path.isfile('.fileStates.data'):
            with open('.fileStates.data', 'rb') as fileState:
                oldFileStates = pickle.load(fileState)
        else:
            oldFileStates = {}
        return(oldFileStates)

    def saveFileStates(self):
        # save file containing dictionary of filenames and their md5 hashes 
        #
        # Args:
        #
        # Return:
        #   sideEffect: saves file ".fileStates.data"
        #
        fileStates = self.getFileStates()
        with open('.fileStates.data', 'wb') as filehandle:
            pickle.dump(fileStates, filehandle)

    def getFileStates(self):
        # generate md5 hashes of files in system and constant  
        #
        # Args:
        #
        # Return:
        #
        fileStates = {}
        for folder in  ["system", "constant", "0.org"]:
            for fileName in os.listdir(folder):
                if os.path.isfile(os.path.join(folder,fileName)):
                    fileStates[os.path.join(folder,fileName)] = md5(os.path.join(folder,fileName))
        if os.path.exists("constant/polyMesh/points"):
            fileStates["constant/polyMesh/points"] = md5("constant/polyMesh/points")
        return(fileStates)

    def compareFileStates(self):
        # compares hashes of files to find changes
        #
        # Args:
        #
        # Return:
        #   fileChangeDict: dict: containing filenames and weather they have changed
        #
        previousFileStates = self.loadFileStates()
        currentFileStates  = self.getFileStates()
        fileChangeDict = {}
        # compare old and new hashes 
        for fileName in currentFileStates:
            if fileName in previousFileStates:
                if currentFileStates[fileName] == previousFileStates[fileName]:
                    fileChangeDict[fileName] = False
                else:
                    fileChangeDict[fileName] = True
            else:
                fileChangeDict[fileName] = True
        return(fileChangeDict)


    ###################################################################
    # graphical output
    ###################################################################

    def printHeader(self):
        # prints header for meshing process
        #
        # Args:
        #
        # Return:
        #
        print("\n==========================================================================")
        print("Solving with OpenFoam %s on %s using %s cores" %(self.foamVer, self.localHost, self.nCores) )
        print("==========================================================================\n")

    def printFooter(self):
        # prints footer for meshing process
        #
        # Args:
        #
        # Return:
        #
        print("\n==========================================================================")
        print("Finished solving in %s" % (datetime.datetime.now()-self.startRun) )
        print("==========================================================================\n")

    def printFooterFailed(self):
        # prints footer for failed meshing process
        #
        # Args:
        #
        # Return:
        #
        print("\n==========================================================================")
        print("Solving failed after %s" % (datetime.datetime.now()-self.startRun))
        print("==========================================================================")

    ###################################################################
    # specialized functions
    ###################################################################

    def clean(self):
        # removes all generated content from a case
        #
        # Args:
        #
        # Return:
        #
        procStart = datetime.datetime.now()
        self.procHandler.printProcStart("Cleaning Case")
        self.procHandler.general(["foamCleanTutorials"])
        if os.path.exists(".fileStates.data"):
            os.remove(".fileStates.data")
        if os.path.exists("doc/runReport/runReport.html"):
            os.remove("doc/runReport/runReport.html")
        self.procHandler.printProcEnd("Cleaning Case", (datetime.datetime.now()-procStart))

    def generateReport(self):
        # generates an RMarkdown report
        #
        # Args:
        #
        # Return:
        #
        cmd = ['R', '-e' , 'rmarkdown::render(\'doc/runReport/runReport.Rmd\')']
        text = "Generating run report"
        logFilePath = os.path.join("log",str("runReport" + ".log"))
        self.procHandler.general(cmd, text, logFilePath)      

    ###################################################################
    # routines
    ###################################################################

    def run(self):
        try:
            self.startRun = datetime.datetime.now()
            self.printHeader()
            if self.runDecomposePar:
                self.procHandler.foam("decomposePar", serial = True)
            if self.runRenumberMesh:
                self.procHandler.foam("renumberMesh", "-overwrite")
            if self.runPotentialFoam:
                self.procHandler.foam("potentialFoam")
            if self.runSolver:
                self.procHandler.foam(self.solver)
            if self.runReconstructPar:
                self.procHandler.foam("reconstructPar", "-newTimes", serial=True)
            if self.runFoamLog:
                files = []
                # find all files which match ident and have the ending .log
                subFiles = [f.name for f in os.scandir("./log") if f.is_file()]
                for fileName in subFiles:
                    if fnmatch.fnmatch(fileName, self.solver + "*.log"):
                        files.append(fileName)
                # add path to each file
                files = [os.path.join("./log", f) for f in files]
                files.sort(key=lambda x: os.path.getmtime(x))
                NewestSolverLog = files[-1]
                self.procHandler.foam("foamLog", NewestSolverLog, serial=True)    
            if self.runReport:
                self.generateReport()
        except AssertionError:
            self.printFooterFailed()
            self.saveFileStates()
        else:
            self.printFooter()
            self.saveFileStates()

    def view(self):
        print("Starting paraFoam")
        if self.nCores > 1:
            self.procHandler.general(["paraFoam", "-builtin"], wait = False)
        else:
            self.procHandler.general(["paraFoam"], wait = False)

###################################################################
# Main Programm
###################################################################

entryPoint = sys.argv[1]
runner = foamRunner()

if entryPoint == "run":
    runner.run()
if entryPoint == "cleanRun":
    runner.clean()
    builder = openFoam.cfdAspectSelector()
    builder.makeSymlinks()
if entryPoint == "view":
    runner.view()