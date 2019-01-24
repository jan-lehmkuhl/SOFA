#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Sebastian Tueck                                             #
# Last Change: January 11 2019                                             #
# Topic:       Meshing process                                             #
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

def createDirSafely(dst):
    # creates a directory recursively if it doesn't exist
    #
    # Args:
    #   dst:   the path to the directory
    #
    # Return:
    #   side effects
    #
    if not os.path.isdir(dst):
        os.makedirs(dst)
        print("Creating >%s<" % dst)
    else:
        print("Skipping >%s< since it already exists" % dst)

def loadJson(jsonPath):
    # Loads a passed .json file if it exists
    #
    # Args:
    #   jsonPath:   s: the path to a Json file
    #
    # Return:
    #   jsonPy:     d: parsed json
    #
    if os.path.exists(jsonPath):
        with open(jsonPath, 'r') as jsonFile:
            jsonPy = json.load(jsonFile)
            return(jsonPy)
    else:
        print("json file >%s< does not exis" % jsonPath)

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
    if value.lower() in ["y", "yes", "true"]:
        return(True)
    elif value.lower() in ["n","no", "false"]:
        return(False)
    else:
        print("Unknown value >%s< please enter True or False" % value)
        sys.exit(0)

class foamMesher(object):
    # class for openFoam meshing procedures

    def __init__(self):
        self.startMeshing = datetime.datetime.now()  
        self.foamVer = checkFoamVer()
        self.localHost = os.uname()[1]
        self.meshJson = loadJson("mesh.json")
        self.nCores = int(self.meshJson["nCores"])
        self.nProcFolder = self.getNoProcFolder()
        self.fileChangeDict = self.compareFileStates()
        self.settings = self.meshJson["meshSettings"]
        self.settingsBlockMesh = boolChecker(self.settings["blockMesh"])
        self.settingsSurfaceFeatures = boolChecker(self.settings["surfaceFeatures"])
        self.settingsSnappyHexMesh = boolChecker(self.settings["snappyHexMesh"])
        self.settingsCheckMesh = boolChecker(self.settings["checkMesh"])
        self.settingsTopoSet = boolChecker(self.settings["topoSet"])
        self.settingsCreatePatches = boolChecker(self.settings["createPatches"])
        self.settingsReport = boolChecker(self.settings["report"])
        if self.settingsBlockMesh:
            if self.fileChangeDict["blockMeshDict"] or self.fileChangeDict["points"]:
                self.runBlockMesh = True
            else:
                self.runBlockMesh = False
        else:
            self.runBlockMesh = False
        if self.nCores > 1:
            if self.fileChangeDict["decomposeParDict"]:
                self.runDecomposePar = True
            elif self.runBlockMesh:
                self.runDecomposePar = True
            else:
                self.runDecomposePar = False
        else:
            self.runDecomposePar = False
        

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

    ###################################################################
    # process handler
    ###################################################################

    def processHandler(self, cmd, text = None, logFilePath = None, wait = True):
        # wrapper around subprocess. takes a list of commands 
        # and excecutes them in bash while optionally
        # displaying a provided text and after excecution the 
        # duration of the process. If a path is specified the output
        # of the process will be redirected to that location.
        # Will also terminate the script if the process fails.
        #
        # Args:
        #   cmd:                list: commands to be excecuted
        #   text (opt.):        str: text to display while excecuting
        #   logFilePath (opt.): str: path where to redirect the output
        #
        # Return:
        #
        start = datetime.datetime.now()           
        if text:
            self.printProcStart(text)
        if logFilePath:
            if not os.path.exists(os.path.dirname(logFilePath)):
              os.makedirs(os.path.dirname(logFilePath))
            with open(logFilePath, 'w') as logfile:
                proc = subprocess.Popen(cmd, stdout = logfile, stderr = subprocess.STDOUT)
                if wait:
                    proc.wait()
        else:
            with open(os.devnull, "w") as f:
                proc = subprocess.Popen(cmd, stdout = f, stderr = subprocess.STDOUT)
                if wait:
                    proc.wait()
        status = proc.returncode
        end = datetime.datetime.now()
        if status == 0:
            if text:
                self.printProcEnd(text, (end-start))
        else:
            if text:
                self.printProcFailed(text, (end-start))
                self.printFooterFailed()
            sys.exit(0)

    def foamProcessHandler(self, process, option = None, serial = False):
        # wrapper of processHandler for openFoam processes 
        #
        # Args:
        #   process:        str:openFoam programm
        #   option (opt.):  str:option for programm 
        #   serial (opt.):  bool: overwrite parallel running
        #
        # Return:
        #
        text = str("Excecuting " + process)
        logFilePath = str("log/" + process + ".log")
        if self.nCores == 1 or serial:
            if option:
                cmd = [process, option]
            else:
                cmd = [process]
        else:
            if option:
                cmd = ["mpirun", "-np", str(self.nCores), process, option, "-parallel"]
            else:
                cmd = ["mpirun", "-np", str(self.nCores), process, "-parallel"]
        self.processHandler(cmd, text, logFilePath) 

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
        print("Meshing boundary layers with OpenFoam %s on %s using %s cores" %(self.foamVer, self.localHost, self.nCores) )
        print("==========================================================================\n")

    def printFooterMesh(self):
        # prints footer for meshing process
        #
        # Args:
        #
        # Return:
        #
        if 'Failed' in open("log/checkMesh.log").read():
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

    def printProcStart(self, text):
        # prints formated text during excecution. Next output
        # will overwrite this
        #
        # Args:
        #   text:   str: text to be displayed during excecution
        #
        # Return:
        #
        sys.stdout.write(" - {0:<30s}\r".format(text))

    def printProcEnd(self, text, duration):
        # prints formated text after excecution
        #
        # Args:
        #   text:       str: text to be displayed during excecution
        #   duration:   str: excecution time
        #
        # Return:
        #
        sys.stdout.flush()
        sys.stdout.write(" - {0:<30s} --> finished after {1:25s}\n".format(text, str(duration)))

    def printProcFailed(self, text, duration):
        # prints formated text after failure
        #
        # Args:
        #   text:       str: text to be displayed during excecution
        #   duration:   str: excecution time
        #
        # Return:
        #
        sys.stdout.flush()
        sys.stdout.write(" - {0:<30s} --> failed after {1:25s}\n".format(text, str(duration)))

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
        self.printProcStart("Cleaning Case")
        self.processHandler(["foamCleanTutorials"])
        self.processHandler(["foamCleanPolyMesh"])
        if os.path.exists(".fileStates.data"):
            os.remove(".fileStates.data")
        if os.path.exists("doc/meshReport/meshReport.html"):
            os.remove("doc/meshReport/meshReport.html")
        self.printProcEnd("Cleaning Case", (datetime.datetime.now()-procStart))

    def generateReport(self):
        # generates an RMarkdown report
        #
        # Args:
        #
        # Return:
        #
        cmd = ['R', '-e' , 'rmarkdown::render(\'doc/meshReport/meshReport.Rmd\')']
        text = "Generating mesh report"
        logFilePath = os.path.join("log",str("MeshReport" + ".log"))
        self.processHandler(cmd, text, logFilePath)

    def removeBoundaryDirs(self):
        # removes all timfolder above 2
        #
        # Args:
        #
        # Return:
        #
        procStart = datetime.datetime.now()
        self.printProcStart("Removing previous layers")
        timeDir = [f for f in os.listdir('.') if fnmatch.fnmatch(f, "[3:9]")]
        procDir = [f for f in os.listdir('.') if fnmatch.fnmatch(f, "processor*")]
        for dirName in timeDir:
            shutil.rmtree(dirName)
        for procName in procDir:
            procTimeDirs = [f for f in os.listdir(procName) if fnmatch.fnmatch(f, "[3:9]")]
            for procTimeDir in procTimeDirs:
                shutil.rmtree(os.path.join(procName,procTimeDir))
        self.printProcEnd("Removing previous layers", (datetime.datetime.now()-procStart))
        

    ###################################################################
    # routines
    ###################################################################

    def mesh(self):
        self.startMeshing = datetime.datetime.now()
        self.printHeaderMesh()
        if self.runBlockMesh or self.runDecomposePar:
            self.clean()
        if self.settingsSurfaceFeatures:
            self.foamProcessHandler("surfaceFeatures", serial = True)
        if self.runBlockMesh:
            self.foamProcessHandler("blockMesh", serial = True)
            if os.path.exists("dynamicCode"):
                shutil.rmtree("dynamicCode")
        if self.runDecomposePar:
            self.processHandler(["foamDictionary", "system/decomposeParDict", "-entry", "numberOfSubdomains", "-set", str(self.nCores)])
            self.processHandler(["foamDictionary", "system/decomposeParDict", "-entry", "method", "-set", "scotch"])
            self.foamProcessHandler("decomposePar", serial = True)
        if self.settingsSnappyHexMesh:
            self.foamProcessHandler("snappyHexMesh")
        if self.settingsCreatePatches:
            self.foamProcessHandler("createPatch")
        if self.settingsTopoSet:
            self.foamProcessHandler("topoSet")
        if self.settingsCheckMesh:
            self.foamProcessHandler("checkMesh", "-meshQuality")
        if self.settingsReport:
            self.generateReport()
        self.saveFileStates()
        self.printFooterMesh()

    def meshLayer(self):
        self.startMeshing = datetime.datetime.now()
        self.printHeaderLayer()
        self.removeBoundaryDirs()
        self.processHandler(["foamDictionary", "system/snappyHexMeshDict", "-entry", "castellatedMesh", "-set", "false"])
        self.processHandler(["foamDictionary", "system/snappyHexMeshDict", "-entry", "snap", "-set", "false"])
        self.processHandler(["foamDictionary", "system/snappyHexMeshDict", "-entry", "addLayers", "-set", "true"])        
        self.foamProcessHandler("snappyHexMesh")
        self.processHandler(["foamDictionary", "system/snappyHexMeshDict", "-entry", "castellatedMesh", "-set", "true"])
        self.processHandler(["foamDictionary", "system/snappyHexMeshDict", "-entry", "snap", "-set", "true"])
        self.foamProcessHandler("checkMesh", "-meshQuality")
        self.generateReport()
        self.saveFileStates()
        self.printFooterMesh()

    def cleanMesh(self):
        self.startMeshing = datetime.datetime.now()
        self.clean()

    def view(self):
        print("Starting paraFoam")
        if self.nCores > 1:
            self.processHandler(["paraFoam", "-builtin"], wait = False)
        else:
            self.processHandler(["paraFoam"], wait = False)

###################################################################
# Main Programm
###################################################################

entryPoint = sys.argv[1]
mesher = foamMesher()

if entryPoint == "mesh":
    mesher.mesh()
if entryPoint == "cleanMesh":
    mesher.cleanMesh()
if entryPoint == "meshLayer":
    mesher.meshLayer()
if entryPoint == "view":
    mesher.view()