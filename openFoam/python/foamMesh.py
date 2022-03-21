#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Sebastian Tueck                                             #
# Last Change: February 01 2019                                            #
# Topic:       Meshing process                                             #
#--------------------------------------------------------------------------#

import sys
import os
import time
import argparse
import shutil
import datetime
import hashlib
import pickle
import fnmatch

# add paths
file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.realpath( file_path +'/../../src' ) ) 

from fileHandling import createDirSafely
from fileHandling import createSymlinkSavely
from fileHandling import copyFileSafely
from fileHandling import copyFolderSafely
from fileHandling import loadJson

from procHandling import procHandler

from case import Case


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

def boolChecker(value, variable):
    # takes a str and checkes if it is a bool and then converts 
    #
    # Args:
    #   value:  str: potential bool
    #
    # Return:
    #   bool:
    #
    if value.lower() in ["y", "yes", "true"]:
        return(True)
    elif value.lower() in ["n","no", "false"]:
        return(False)
    else:
        print("Unknown value >%s< for variable >%s<. Please enter True or False" %(value, variable))
        sys.exit(0)

class foamMesher(object):
    # class for openFoam meshing procedures

    def __init__(self, verbose):
        self.startMeshing = datetime.datetime.now()
        self.case = Case( )
        self.verbose = verbose
        self.foamVer = checkFoamVer()
        self.localHost = os.uname()[1]
        self.nProcFolders = self.getNoProcFolder()
        self.fileChangeDict = self.compareFileStates()
        # extract mesh settings
        self.meshSettings = self.case.caseJson['meshSettings']
        # extract variables mesh settings and assign it to a variable
        self.nCores                  = int(self.meshSettings['nCores'])
        self.settingsBlockMesh       = boolChecker(self.meshSettings["blockMesh"], "blockMesh")
        self.settingsSurfaceFeatures = boolChecker(self.meshSettings["surfaceFeatures"], "surfaceFeatures")
        self.settingsSnappyHexMesh   = boolChecker(self.meshSettings["snappyHexMesh"], "snappyHexMesh")
        self.settingsCheckMesh       = boolChecker(self.meshSettings["checkMesh"], "checkMesh")
        self.settingsTopoSet         = boolChecker(self.meshSettings["topoSet"], "topoSet")
        self.settingsCreatePatches   = boolChecker(self.meshSettings["createPatches"], "createPatches")
        self.settingsReport          = boolChecker(self.meshSettings["report"],"report" )
        # initialize variables determining weather to run a program or not 
        self.runBlockMesh       = self.settingsBlockMesh       
        self.runSurfaceFeatures = self.settingsSurfaceFeatures 
        self.runSnappyHexMesh   = self.settingsSnappyHexMesh   
        self.runCheckMesh       = self.settingsCheckMesh
        self.runTopoSet         = self.settingsTopoSet         
        self.runCreatePatches   = self.settingsCreatePatches
        self.runReport          = self.settingsReport          
        # instantiate process handler with number 
        self.procHandler = procHandler(self.nCores)
        # run blockmesh logic
        if self.settingsBlockMesh:
            # if blockMeshDict or mesh changed run blockMesh
            if self.fileChangeDict["blockMeshDict"] or self.fileChangeDict["points"]:
                self.runBlockMesh = True
            # if nothing changed don't run blockMesh
            else:
                self.runBlockMesh = False
        else:
            self.runBlockMesh = False
        # run decomposePar logic 
        if self.nCores > 1:
            # run if  decomposePar changed
            if self.fileChangeDict["decomposeParDict"]:
                self.runDecomposePar = True
            # run if blockMesh changed
            elif self.runBlockMesh:
                self.runDecomposePar = True
            # skip if nothing changed
            else:
                self.runDecomposePar = False
        else:
            self.runDecomposePar = False
        # run surfaceFeatures 
        if (self.settingsSurfaceFeatures and 
            os.path.exists("constant/triSurface") ):
            # check weather surface features are present
            featureEdgesPresent = False     # init
            for fileName in os.listdir("constant/triSurface"):
                if fnmatch.fnmatch(fileName, "*.eMesh"):
                    featureEdgesPresent = True
                    break
            # don't run if surfaceFeaturesDict didn't change
            if 'surfaceFeaturesDict' in self.fileChangeDict :
                if not self.fileChangeDict["surfaceFeaturesDict"] and featureEdgesPresent:
                    self.runSurfaceFeatures = False
                else: 
                    self.runSurfaceFeatures = True
            elif 'surfaceFeatureExtractDict' in self.fileChangeDict :
                if not self.fileChangeDict["surfaceFeatureExtractDict"] and featureEdgesPresent:
                    self.runSurfaceFeatures = False
                else: 
                    self.runSurfaceFeatures = True
            else:
                print("neiter surfaceFeatures or surfaceFeaturesExtract exist")
            if self.runSurfaceFeatures == True :
                print("decided to run surface features")            


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
        for folder in  ["system", "constant"]:
          if os.path.exists(folder):
            for fileName in os.listdir(folder):
                if os.path.isfile(os.path.join(folder,fileName)):
                    fileStates[fileName] = md5(os.path.join(folder,fileName))
        if os.path.exists("constant/polyMesh/points"):
            fileStates["points"] = md5("constant/polyMesh/points")
        else:
            fileStates["points"] = ""
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
    
    def latestLogFile(self, path, ident):
        # lists all files matching "ident" and write them into a single file
        # in order of modification date
        #
        # Args :
        #   path:   path to folder to look in
        #   ident:  identifiert for type of logfile ("snappyHexMesh")
        #
        # Return :
        #   sideEffect:    writes out new logfile
        #

        nChar = len(ident)
        files = []
        # find all files which match ident and have the ending .log
        subFiles = [f.name for f in os.scandir(path) if f.is_file()]
        for fileName in subFiles:
            if (fileName[:nChar] == ident and fileName[-4:] == ".log"):
                files.append(fileName)

        files = [os.path.join(path, f) for f in files]
        files.sort(key=lambda x: os.path.getmtime(x))

        return(files[-1])

    ###################################################################
    # graphical output
    ###################################################################

    def printHeaderMesh(self):
        # prints header for meshing process
        #
        # Args:
        #
        # Return:
        #
        print("\n==========================================================================")
        print("Meshing with OpenFoam %s on %s using %s cores" %(self.foamVer, self.localHost, self.nCores) )
        print("==========================================================================\n")

    def printHeaderLayer(self):
        # prints header for layering process
        #
        # Args:
        #
        # Return:
        #
        print("\n==========================================================================")
        print("Meshing boundary layers with OpenFoam %s on %s" %(self.foamVer, self.localHost) )
        print("==========================================================================\n")
    
    def printHeaderFinalize(self):
        # prints header for layering process
        #
        # Args:
        #
        # Return:
        #
        print("\n==========================================================================")
        print("Finalizing mesh with OpenFoam %s on %s using %s cores" %(self.foamVer, self.localHost, self.nCores) )
        print("==========================================================================\n")

    def printFooterMesh(self):
        # prints footer for meshing process
        #
        # Args:
        #
        # Return:
        #
        checkMeshFile = self.latestLogFile("./log", "checkMesh")
        if 'Failed' in open(checkMeshFile).read():
            meshQuality = '\033[91m' + "flawed" + '\033[0m'
        else:
            meshQuality = '\033[32m' + "good" + '\033[0m'
        print("\n==========================================================================")
        print("Finished mesh with %s quality in %s" %( meshQuality, (datetime.datetime.now()-self.startMeshing) ))
        print("==========================================================================\n")

    def printFooterFailed(self):
        # prints footer for failed meshing process
        #
        # Args:
        #
        # Return:
        #
        print("\n==========================================================================")
        print("Meshing failed after %s" % (datetime.datetime.now()-self.startMeshing))
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
        self.procHandler.general(["foamCleanPolyMesh"])
        if os.path.exists(".fileStates.data"):
            os.remove(".fileStates.data")
        if os.path.exists("doc/meshReport/meshReport.html"):
            os.remove("doc/meshReport/meshReport.html")
        self.procHandler.printProcEnd("Cleaning Case", (datetime.datetime.now()-procStart))

    def generateReport(self):
        # generates an RMarkdown report
        #
        # Args:
        #
        # Return:
        #
        cmd = ['R', '-e' , 'rmarkdown::render(\'doc/meshReport/meshReport.Rmd\')']
        text = "Generating mesh report"
        logFilePath = os.path.join("log",str("meshReport" + ".log"))
        self.procHandler.general(cmd, text, logFilePath)

    def removeBoundaryDirs(self):
        # removes all timfolder above 2
        #
        # Args:
        #
        # Return:
        #
        procStart = datetime.datetime.now()
        self.procHandler.printProcStart("Removing previous layers")
        timeDir = [f for f in os.listdir('.') if fnmatch.fnmatch(f, "[3:9]")]
        procDir = [f for f in os.listdir('.') if fnmatch.fnmatch(f, "processor*")]
        for dirName in timeDir:
            shutil.rmtree(dirName)
        for procName in procDir:
            procTimeDirs = [f for f in os.listdir(procName) if fnmatch.fnmatch(f, "[3:9]")]
            for procTimeDir in procTimeDirs:
                shutil.rmtree(os.path.join(procName,procTimeDir))
        self.procHandler.printProcEnd("Removing previous layers", (datetime.datetime.now()-procStart))
        

    ###################################################################
    # routines
    ###################################################################

    def mesh(self):
        try:
            self.startMeshing = datetime.datetime.now()
            self.printHeaderMesh()
            if self.runBlockMesh or self.runDecomposePar:
                self.clean()
            if self.runSurfaceFeatures:
                if 'surfaceFeaturesDict' in self.fileChangeDict :
                    self.procHandler.foam("surfaceFeatures", serial = True)
                elif 'surfaceFeatureExtractDict' in self.fileChangeDict :
                    self.procHandler.foam("surfaceFeatureExtract", serial = True)
                else:
                    print("no surfaceFeatures or surfaceFeatureExtract defined")
            if self.runBlockMesh:
                self.procHandler.foam("blockMesh", serial = True)
                if os.path.exists("dynamicCode"):
                    shutil.rmtree("dynamicCode")
            if self.runDecomposePar:
                self.procHandler.general(["foamDictionary", "system/decomposeParDict", "-disableFunctionEntries", "-entry", "numberOfSubdomains", "-set", str(self.nCores)])
                self.procHandler.general(["foamDictionary", "system/decomposeParDict", "-disableFunctionEntries", "-entry", "method", "-set", "scotch"])
                self.procHandler.foam("decomposePar", serial = True)
            if self.settingsSnappyHexMesh:
                self.procHandler.foam("snappyHexMesh")
            if self.settingsCreatePatches:
                self.procHandler.foam("createPatch")
            if self.settingsTopoSet:
                self.procHandler.foam("topoSet")
            if self.settingsCheckMesh:
                self.procHandler.foam("checkMesh", "-meshQuality")
            if self.settingsReport:
                self.generateReport()
        except AssertionError:
            self.printFooterFailed()
            self.saveFileStates()
        else:
            self.printFooterMesh()
            self.saveFileStates()

    def meshLayer(self):
        self.startMeshing = datetime.datetime.now()
        self.printHeaderLayer()
        self.removeBoundaryDirs()
        self.procHandler.general(["foamDictionary", "system/snappyHexMeshDict", "-disableFunctionEntries", "-entry", "castellatedMesh", "-set", "false"])
        self.procHandler.general(["foamDictionary", "system/snappyHexMeshDict", "-disableFunctionEntries", "-entry", "snap", "-set", "false"])
        self.procHandler.general(["foamDictionary", "system/snappyHexMeshDict", "-disableFunctionEntries", "-entry", "addLayers", "-set", "true"])        
        self.procHandler.foam("snappyHexMesh")
        self.procHandler.general(["foamDictionary", "system/snappyHexMeshDict", "-disableFunctionEntries", "-entry", "castellatedMesh", "-set", "true"])
        self.procHandler.general(["foamDictionary", "system/snappyHexMeshDict", "-disableFunctionEntries", "-entry", "snap", "-set", "true"])
        self.procHandler.foam("checkMesh", "-meshQuality")
        self.generateReport()
        self.saveFileStates()
        self.printFooterMesh()

    def cleanMesh(self):
        self.startMeshing = datetime.datetime.now()
        self.clean()

    def finalizeMesh(self):
        self.startMeshing = datetime.datetime.now()
        self.printHeaderFinalize()
        if not self.nProcFolders == 0:
            self.procHandler.general(["reconstructParMesh", "-latestTime"], "Reconstructing final mesh")
        timeDirs = [f for f in os.listdir('.') if fnmatch.fnmatch(f, "[1,2,3,4,5,6,7,8,9]")]
        latestTime = max(timeDirs)
        start = datetime.datetime.now()
        self.procHandler.printProcStart("Copying mesh")
        if os.path.exists("constant/polyMesh"):
            shutil.rmtree("constant/polyMesh")
        shutil.copytree(os.path.join(latestTime, "polyMesh"), "constant/polyMesh")
        self.procHandler.printProcEnd("Copying mesh", (datetime.datetime.now() - start))
        self.printFooterMesh()      

    def view(self):
        print("Starting paraFoam")
        if self.nCores > 1:
            self.procHandler.general(["paraFoam", "-builtin"], wait = False)
        else:
            self.procHandler.general(["paraFoam"], wait = False)

###################################################################
# Main Programm
###################################################################

# read arguments and options from command line
parser = argparse.ArgumentParser(description='input for foamMesher.py')
parser.add_argument( 'entryPoint',      help="chose the task for this python script" ) 
parser.add_argument( '--verbose', '-v', action="store_true", dest="verbose", default=False )

entryPoint = sys.argv[1]
mesher = foamMesher( verbose=parser.parse_args().verbose )

if entryPoint == "mesh":
    mesher.mesh()
if entryPoint == "cleanMesh":
    mesher.cleanMesh()
if entryPoint == "meshLayer":
    mesher.meshLayer()
if entryPoint == "view":
    mesher.view()
if entryPoint == "finalizeMesh":
    mesher.finalizeMesh()
