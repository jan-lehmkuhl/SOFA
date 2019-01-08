#!/usr/bin/env python3

# import librarys
import json
import os
import sys
import shutil

foamStructure = {
    "cad":      {"studyName": "01cad"},
    "mesh":     {"studyName": "02mesh",        "linkName": "cadLink",     "linkType": "cad"},
    "run":      {"studyName": "03run",         "linkName": "meshLink",    "linkType": "mesh"},
    "analysis": {"studyName": "04analysis",    "linkName": "caseLinks",   "linkType": "run"}
}


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


def copyFileSafely(src, dst):
    # copies a file if it exists
    #
    # Args:
    #   src:   s: path to the file to be copied
    #   dst:   s: path to copy the file to
    #
    # Return:
    #   side effects
    #
    if os.path.exists(src):
        if not os.path.isdir(src):
            if not os.path.exists(dst):
                shutil.copyfile(src, dst)
                print("Copying file from >%s< to >%s<" % (src, dst))
            else:
                print("Skipping >%s< since it already exists" % src)
        else:
            print("Skipping >%s< because it is a directory" % src)
    else:
        print("Unabel to find >%s<" % src)


def createSymlinkSavely(src, dst):
    # creates a symbolic link between src and dst if the source
    # exists and the dst doesn't. If dst exists but is already
    # a symbolic link it is overwritten.
    #
    # Args:
    #   src:    s: path to the source file from current destination
    #   dst:    s: path the the destination from current destination
    #
    # Return:
    #   side effects
    #
    if os.path.exists(src):
        relSrc = os.path.relpath(src, os.path.dirname(dst))
        if not os.path.exists(dst):
            os.symlink(relSrc, dst)
            print("Creating link from >%s< to >%s<" % (src, dst))
        elif os.path.islink(dst):
            if not os.readlink(dst) == relSrc:
                os.remove(dst)
                os.symlink(relSrc, dst)
                print(
                    "Overwriting existing link with link from >%s< to >%s<" % (src, dst))
            else:
                print("Skipping link to >%s< because it already exists" % src)
        else:
            print("Unabel to create target >%s< since it exists" % dst)
    else:
        print("Unabel to find >%s<" % src)


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


def findFile(fileName, turnFolder):
    # traverses a tree upwards till it finds turnfolder and then dives into
    # turnfolder till it finds file
    #
    # Args:
    #   fileName:   s: name of the file that is searched for
    #   turnfolder: s: name of the folder to turn on
    #
    # Return:
    #   path:       s: relative path to the file
    #
    i = 0
    wd = os.getcwd()
    subdirs = os.listdir(os.getcwd())
    while i < 5:
        if turnFolder in subdirs:
            for root, dirs, files in os.walk(os.path.join(wd, turnFolder)):
                if fileName in files:
                    path = os.path.relpath(
                        os.path.join(root, fileName), os.getcwd())
                    return(path)
            else:
                print("Could not find file >%s< in >%s<" %
                      (fileName, os.path.join(wd, turnFolder)))
                return(False)
        wd = os.path.join(wd, os.path.pardir)
        subdirs = os.listdir(wd)
        i += 1
    else:
        print("Could not find folder >%s<" % turnFolder)
        return(False)


def findFolder(folderName, turnFolder):
    # traverses a tree upwards till it finds turnfolder and then dives into
    # turnfolder till it finds folder
    #
    # Args:
    #   folderName: s: name of the folder that is searched for
    #   turnfolder: s: name of the folder to turn on
    #
    # Return:
    #   path:       s: relative path to the file
    #
    i = 0
    wd = os.getcwd()
    subdirs = os.listdir(os.getcwd())
    while i < 5:
        if turnFolder in subdirs:
            for root, dirs, files in os.walk(os.path.join(wd, turnFolder)):
                if folderName in dirs:
                    path = os.path.relpath(
                        os.path.join(root, folderName), os.getcwd())
                    return(path)
            else:
                print("Could not find folder >%s< in >%s<" %
                      (folderName, os.path.join(wd, turnFolder)))
                return(False)
        wd = os.path.join(wd, os.path.pardir)
        subdirs = os.listdir(wd)
        i += 1
    else:
        print("Could not find folder >%s<" % turnFolder)
        return(False)


def caseSelector(path=None):
    # determines the type of the case from the name of the containing folder
    #
    # Args:
    #   path:       s: path to pass
    #
    # Return:
    #   studyName:  s: Name of the containing folder stripped of numbers
    #               this should equal the type
    #
    if path is None:
        path = "./"
        studyFolder = os.path.basename(os.getcwd())
    else:
        studyFolder = os.path.basename(path)
    studyName = ''.join(
        [i for i in studyFolder if not i.isdigit()])  # remove digits
    if studyName in foamStructure:
        if studyName == "cad":
            return(CadCase(path))
        elif studyName == "mesh":
            return(MeshCase(path))
        elif studyName == "run":
            return(RunCase(path))
        elif studyName == "analysis":
            return(AnalysisCase(path))
    else:
        print("Unknown study type >%s<" % studyName)
        return(False)


class Study(object):
    # base class to handle all operations related to studys

    global foamStructure

    def __init__(self, type, path="./"):
        self.type = type
        self.path = path
        self.name = "Study"

    def create(self):
        # creates a study of self.type at location self.path
        # according to the entrys in the global dictionary foamStructure
        #
        # Args:
        #
        # Return:
        #   side effects: creates study
        #
        studyName = foamStructure[self.type]["studyName"]
        createDirSafely(os.path.join(self.path, studyName))
        makefilePath = findFile("Makefile_study", "tools")
        if makefilePath:  # if find file fails it returns false
            #copyFileSafely(makefilePath, os.path.join(self.path, studyName, "Makefile"))
            createSymlinkSavely(makefilePath, os.path.join(
                self.path, studyName, "Makefile"))
            case = caseSelector(os.path.join(self.path, studyName))
            case.create()


class Case(object):
    # base class to handle all operations related to cases

    global foamStructure

    def __init__(self, type=None, path="./"):
        self.name = "Case"
        self.type = type
        self.path = path
        self.caseJson = None
        self.linkedCase = None
        self.pathToLinkedCase = None
        self.symlinksClean = False
        if os.path.exists(self.path + self.type + ".json"):
            self.caseJson = loadJson(self.type + ".json")
            self.linkedCase = self.caseJson[foamStructure[self.type]["linkName"]]
            if self.linkedCase:
                if isinstance(self.linkedCase, str):
                    self.pathToLinkedCase = findFolder(
                        self.linkedCase, foamStructure[foamStructure[self.type]["linkType"]]["studyName"])
                elif isinstance(self.linkedCase, list):
                    self.pathToLinkedCase = []
                    for element in self.linkedCase:
                        self.pathToLinkedCase.append(findFolder(
                            element, foamStructure[foamStructure[self.type]["linkType"]]["studyName"]))
                else:
                    print(
                        "Unexpected type of self.linkPath in __init__ of %s" % self.name)

    def nextCaseName(self, path="./"):
        # finds the next case name in a series of folder of type xxx123
        #
        # Args:
        #   path:   path to folder to look in
        #
        # Return:
        #   name:   name of the next case folder
        #
        subfolders = [f.name for f in os.scandir(path) if f.is_dir()]
        maxNo = 0
        charCount = len(self.type)
        for folder in subfolders:
            if folder[:charCount] == self.type:
                currentNo = int(folder[charCount:])
                if currentNo > maxNo:
                    maxNo = currentNo
        CaseName = str(self.type + format(maxNo + 1, "0>3d"))
        return(CaseName)

    def getProject(self):
        # finds the projectname of a case
        #
        # Args:
        #
        # Return:
        #   name:   name of the next case folder
        #
        i = 0
        wd = os.getcwd()
        subdirs = os.listdir(os.getcwd())
        while i < 5:
            if foamStructure["cad"]["studyName"] in subdirs:
                return(os.path.basename(os.path.normpath(wd)))
            else:
                wd = os.path.join(wd, os.path.pardir)
                subdirs = os.listdir(wd)
                i += 1
        else:
            print("Could not find project name")
            return(False)

    def create(self):
        # create a new case inside a study depending on the type of case
        #
        # Args:
        #
        # Return:
        #   side effects
        #
        jsonPath = findFile(self.type + ".json", "tools")
        makePath = findFile("Makefile_case", "tools")
        gitignorePath = findFile(".gitignore_foam", "tools")
        caseName = self.nextCaseName()
        if (jsonPath and makePath):
            createDirSafely(os.path.join(self.path, caseName))
            #copyFileSafely(makePath, os.path.join(self.path, caseName, "Makefile"))
            createSymlinkSavely(makePath, os.path.join(
                self.path, caseName, "Makefile"))
            copyFileSafely(jsonPath, os.path.join(
                self.path, caseName, self.type + ".json"))
            createSymlinkSavely(gitignorePath, os.path.join(
                self.path, caseName, ".gitignore"))
        return(True)

    def clone(self):
        # create a clone of the current case
        #
        # Args:
        #
        # Return:
        #   side effects: makes a clone of the case
        #
        currentCase = os.path.basename(os.getcwd())
        caseName = self.nextCaseName(os.pardir)
        path = os.path.join(os.pardir, caseName)
        print("Cloning case >%s< to >%s<" % (currentCase, caseName))
        shutil.copytree(os.path.join(os.pardir, currentCase),
                        path, symlinks=True)
        while True:
            print("Commit cloning of >%s< to >%s< ? (y/n)" %
                  (currentCase, caseName))
            answer = input()
            answer = answer.lower()
            if answer in ["y", "yes"]:
                projName = self.getProject()
                os.system('git add %s' % path)
                os.system('git commit -m "[%s%s] #CLONE \'cloning case >%s< to >%s<\'"' % (
                    projName, caseName.capitalize(), currentCase, caseName))
                break
            elif answer in ["n", "no"]:
                break

    def clear(self):
        # removes all files, folders and symlinks from a case, but spares
        # out the Makefile and the .json file of the case
        #
        # Args:
        #
        # Return:
        #   side effects: removes folders
        #
        caseName = os.path.basename(os.getcwd())
        while True:
            print("Do you really want to clear case >%s< ? (y/n)" % caseName)
            answer = input()
            answer = answer.lower()
            if answer in ["y", "yes"]:
                for root, dirs, files in os.walk("./", topdown=False):
                    for name in files:
                        if name == "Makefile":
                            continue
                        if name == ".gitignore":
                            continue
                        elif name.endswith("json"):
                            continue
                        else:
                            os.remove(os.path.join(root, name))
                            print("Removing file >%s< from case" %
                                  os.path.join(root, name))
                    for name in dirs:
                        if os.path.islink(os.path.join(root, name)):
                            os.remove(os.path.join(root, name))
                            print("Removing link >%s<" %
                                  os.path.join(root, name))
                        else:
                            os.rmdir(os.path.join(root, name))
                            print("Removing folder >%s< from case" %
                                  os.path.join(root, name))
                while True:
                    print("Commit clearing of %s ? (y/n)" % caseName)
                    answer = input()
                    answer = answer.lower()
                    if answer in ["y", "yes"]:
                        projName = self.getProject()
                        os.system('git add .')
                        os.system('git commit -m "[%s%s] #CLEAR \'cleared case >%s< in project >%s<\'"' 
                                  % (projName, caseName.capitalize(), caseName, projName))
                        break
                    elif answer in ["n", "no"]:
                        break
                break
            elif answer in ["n", "no"]:
                break

    def makeMainSymlink(self):
        # links the folder stated in the case json into the directory
        #
        # Args:
        #
        # Return:
        #   side effects:  creates the main symlink
        #
        # make sure symlinks are clean but avoid double calling
        if not self.symlinksClean:
            self.removeSymlinks
        # check if a file to link to has been specified in *.json file
        if self.linkedCase:
            # check if the file to link to exists
            if self.pathToLinkedCase:
                #os.symlink(self.pathToLinkedCase, self.linkedCase)
                createSymlinkSavely(self.pathToLinkedCase, self.linkedCase)
                #print("Create link to >%s<" % self.pathToLinkedCase)
                return(True)
        else:
            print("No link specified for this case yet")
            return(False)

    def removeSymlinks(self):
        # removes the symlinks from a case which have been created
        # by the script
        #
        # Args:
        #
        # Result:
        #   side effects : removes symlinks
        #
        # Lists of folders and extensions to delete
        extensions = [".stl", ".vtk"]
        folder = ["polyMesh", "cadPics", "meshPics",
                  "drafts", "meshReport", "layerSizing"]
        for key in foamStructure:
            folder.append(key)
        # Traverse all subdirectories in case
        for root, dirs, files in os.walk("./"):
            for dirName in dirs:
                if os.path.islink(os.path.join(root, dirName)):
                    # remove digits from foldernames to compare with folder
                    stripped = ''.join([i for i in dirName if not i.isdigit()])
                    if stripped in folder:
                        os.remove(os.path.join(root, dirName))
                        print("Removing link >%s<" %
                              os.path.join(root, dirName))
            for fileName in files:
                if os.path.islink(os.path.join(root, fileName)):
                    # check if file extension is in extensions
                    if os.path.splitext(os.path.join(root, fileName))[1] in extensions:
                        os.remove(os.path.join(root, fileName))
                        print("Removing link >%s<" %
                              os.path.join(root, fileName))
        self.symlinksClean = True

    def commitInit(self):
        # asks user if he wants to commit the initialisation to git
        #
        # Args:
        #
        # Result:
        #   side effects:   commits changes of case
        #
        projName = self.getProject()
        caseName = os.path.basename(os.getcwd())
        while True:
            print("Commit initialisation of %s ? (y/n)" % caseName)
            answer = input()
            answer = answer.lower()
            if answer in ["y", "yes"]:
                projName = self.getProject()
                os.system('git add .')
                os.system('git commit -m "[%s%s] #INIT \'initialised case >%s< in project >%s<\'"' % (
                    projName, caseName.capitalize(), caseName, projName))
                break
            elif answer in ["n", "no"]:
                break

    def commitChanges(self):
        # asks user if he wants to commit changes to case
        #
        # Args:
        #
        # Result:
        #   side effects:   commits changes of case
        #
        caseName = os.path.basename(os.getcwd())
        while True:
            print("Commit changes in %s ? (y/n)" % caseName)
            answer = input()
            answer = answer.lower()
            if answer in ["y", "yes"]:
                while True:
                    print("Please enter a commit message:")
                    message = input()
                    if not message == "":
                        break
                projName = self.getProject()
                os.system('git add .')
                os.system('git commit -m "[%s%s] #CHANGE \'%s\'"' %
                          (projName, caseName.capitalize(), message))
                break
            elif answer in ["n", "no"]:
                break


class CadCase(Case):
    # Specialized class for cad cases, which inherits from the base Case class

    def __init__(self, path="./"):
        super().__init__("cad", path)
        self.name = "CadCase"

    def create(self):
        # specialized method which creates all folders needed in
        # a case of type cad
        #
        # Args:
        #
        # Return:
        #   side effects: creates directories
        #
        caseName = self.nextCaseName()
        createDirSafely(os.path.join(self.path, caseName, "native"))
        createDirSafely(os.path.join(self.path, caseName, "stl"))
        createDirSafely(os.path.join(self.path, caseName, "vtk"))
        createDirSafely(os.path.join(self.path, caseName, "doc/drafts"))
        createDirSafely(os.path.join(self.path, caseName, "doc/cadPics"))
        makePath = findFile("Makefile_case", "tools")
        gitignorePath = findFile(".gitignore_cad", "tools")
        if makePath:
            createSymlinkSavely(makePath, os.path.join(
                self.path, caseName, "Makefile"))
        if gitignorePath:
            createSymlinkSavely(gitignorePath, os.path.join(
                self.path, caseName, ".gitignore"))
        self.commitInit()

    def initCase(self):
        if len(os.listdir(".")) <= 1:
            createDirSafely("native")
            createDirSafely("stl")
            createDirSafely("vtk")
            createDirSafely("doc/drafts")
            createDirSafely("doc/cadPics")
            makePath = findFile("Makefile_case", "tools")
            gitignorePath = findFile(".gitignore_cad", "tools")
            if makePath:
                copyFileSafely(makePath, "Makefile")
            if gitignorePath:
                copyFileSafely(gitignorePath, ".gitignore")
            self.commitInit()
        else:
            print("Case is already initialised. Please run >make clean< first")

    def makeSymlinks(self):
        print("Cases of type >cad< do not support option symlinks")


class MeshCase(Case):
     # Specialized class for cad cases, which inherits from the base Case class

    def __init__(self, path="./"):
        super().__init__("mesh", path)
        self.name = "MeshCase"
        self.Builder = foamBuilder()

    def makeSymlinks(self):
        # specialized method to create all symlinks needed for a case
        # of type mesh
        #
        # Args:
        #
        # Return:
        #   side effects: creates symlinks for mesh
        #
        linkedGeometry = False
        # if symlinks already exist, delete them
        self.removeSymlinks()
        if self.makeMainSymlink():
            createDirSafely("constant/triSurface")
            createDirSafely("doc")
            for extension in ["stl", "vtk"]:
                for element in os.listdir(os.path.join(self.pathToLinkedCase, extension)):
                    if element.endswith("." + extension):
                        createSymlinkSavely(os.path.join(self.pathToLinkedCase, extension, element), os.path.join(
                            "./constant/triSurface/", element))
                        if element.endswith(".stl"):
                            linkedGeometry = True
            for element in os.listdir(os.path.join(self.pathToLinkedCase, "doc")):
                createSymlinkSavely(os.path.join(
                    self.pathToLinkedCase, "doc", element), os.path.join("./doc", element))
            if not linkedGeometry:
                print("WARNING: Did not link to any geometry files")
            return(True)

    def initCase(self):
        # specialised method to initialise a case of type mesh
        #
        # Args:
        #
        # Returns:
        #   side effects: creates directories, copies files makes symlinks
        #
        if os.path.isdir("./system"):
            print(
                "Case is already initialized. If you want to reinitialize please delete >system")
        elif self.makeSymlinks():
            self.Builder.makeMesh()
            createDirSafely("doc/meshReport")
            createDirSafely("doc/layerSizing")
            createDirSafely("doc/meshPics")
            meshReportPath = findFile("MeshReport.Rmd", "tools")
            if meshReportPath:
                copyFileSafely(meshReportPath, "doc/meshReport/meshReport.Rmd")
            layerSizingPath = findFile("LayerSizing.Rmd", "tools")
            if layerSizingPath:
                copyFileSafely(layerSizingPath,
                               "doc/layerSizing/layerSizing.Rmd")
            self.commitInit()


class RunCase(Case):
    # Class for run cases

    def __init__(self, path=None):
        super().__init__("run", path)
        self.name = "RunCase"
        if self.caseJson:
            self.Builder = foamBuilder(self.caseJson["OpenFOAMSettings"])

    def makeSymlinks(self):
        # specialized method to create all symlinks needed for a case
        # of type run
        #
        # Args:
        #
        # Return:
        #   side effects: creates symlinks for run
        #
        self.removeSymlinks()
        if self.makeMainSymlink():
            createDirSafely("constant")
            createDirSafely("doc")
            createSymlinkSavely(os.path.join(
                self.pathToLinkedCase, "constant/polyMesh"), os.path.join("./constant/polyMesh"))
            for element in os.listdir(os.path.join(self.pathToLinkedCase, "doc")):
                currentPath = os.path.join(
                    self.pathToLinkedCase, "doc", element)
                createSymlinkSavely(currentPath, os.path.join("doc", element))
            return(True)

    def initCase(self):
        # specialised method to initialise a case of type run
        #
        # Args:
        #
        # Returns:
        #   side effects: creates directories, copies files makes symlinks
        #
        if os.path.isdir("./system"):
            print(
                "Case is already initialized. If you want to reinitialize please delete >system")
        elif self.makeSymlinks():
            self.Builder.makeBase()
            self.Builder.makeTurbulence()
            self.Builder.makeDynamicMesh()
            self.Builder.makePorousZone()
            self.commitInit()


class AnalysisCase(Case):
    # Class for analysis cases

    def __init__(self, path=None):
        super().__init__("analysis", path)
        self.name = "AnalysisCase"

    def makeSymlinks(self):
        # specialized method to create all symlinks needed for a case
        # of type run
        #
        # Args:
        #
        # Return:
        #   side effects: creates symlinks for run
        #
        self.removeSymlinks()
        if False in self.pathToLinkedCase:
            return(False)
        for element in self.pathToLinkedCase:
            createSymlinkSavely(element, os.path.basename(element))


class foamBuilder(object):
    # class to handle the setup of openFoam folder structures from the
    # foamFiles.json file

    def __init__(self, foamCaseSettings=None):
        self.foamJson = loadJson(findFile("foamFiles.json", "tools"))
        self.setupPath = findFolder("openFoam-setup", "tools")
        self.foamCaseSettings = foamCaseSettings

    def makeMesh(self):
        # reads the file structure from foamFiles.json and copies all nessesary files
        # listed there to create a mesh
        #
        # Args:
        #
        # Return:
        #   side effects: builds an OpenFOAM structure for meshes
        #
        if self.foamJson:
            if self.setupPath:
                meshStruct = self.foamJson["mesh"]
                for folder in meshStruct:
                    createDirSafely(folder)
                    for file in meshStruct[folder]:
                        copyFileSafely(os.path.join(
                            self.setupPath + meshStruct[folder][file]), os.path.join(folder, file))

    def makeBase(self):
        # reads the file structure from foamFiles.json and copies all nessesary files
        # listed there to create the basic structure for a solver given in
        # the run.json file
        #
        # Args:
        #
        # Return:
        #   side effects: builds an OpenFOAM structure for meshes
        #
        if self.foamJson:
            if self.setupPath:
                solver = self.foamCaseSettings["solver"]
                if solver in self.foamJson:
                    baseStruct = self.foamJson[solver]
                    for folder in baseStruct:
                        createDirSafely(folder)
                        for file in baseStruct[folder]:
                            copyFileSafely(os.path.join(
                                self.setupPath + baseStruct[folder][file]), os.path.join(folder, file))
                else:
                    print("Unknown Solver >%s< specified in run.json" % solver)

    def makeTurbulence(self):
        # reads the file structure from foamFiles.json and copies all nessesary files
        # listed there to add the nessessary files for a turbulence model given in
        # the run.json file
        #
        # Args:
        #
        # Return:
        #   side effects: adds turbulence files
        #
        if self.foamJson:
            if self.setupPath:
                turbulenceModell = self.foamCaseSettings["turbulenceModel"]
                if turbulenceModell in self.foamJson["turbulence"]:
                    baseStruct = self.foamJson["turbulence"][turbulenceModell]
                    for folder in baseStruct:
                        createDirSafely(folder)
                        for file in baseStruct[folder]:
                            copyFileSafely(os.path.join(
                                self.setupPath + baseStruct[folder][file]), os.path.join(folder, file))
                else:
                    print("Unknown turbulence model >%s< specified in run.json" %
                          turbulenceModell)

    def makePorousZone(self):
        # reads the file structure from foamFiles.json and copies all nessesary files
        # listed there to add the nessessary files for a porous zone as given in
        # the run.json file
        #
        # Args:
        #
        # Return:
        #   side effects: adds porous zone
        #
        if self.foamJson:
            if self.setupPath:
                porousZone = self.foamCaseSettings["porousZone"]
                if porousZone.lower() in ["true", "yes"]:
                    baseStruct = self.foamJson["porousZone"]
                    for folder in baseStruct:
                        createDirSafely(folder)
                        for file in baseStruct[folder]:
                            copyFileSafely(os.path.join(
                                self.setupPath + baseStruct[folder][file]), os.path.join(folder, file))

    def makeDynamicMesh(self):
        # reads the file structure from foamFiles.json and copies all nessesary files
        # listed there to add the nessessary files for a porous zone as given in
        # the run.json file
        #
        # Args:
        #
        # Return:
        #   side effects: adds porous zone
        #
        if self.foamJson:
            if self.setupPath:
                dynamicMesh = self.foamCaseSettings["dynamicMesh"]
                if dynamicMesh.lower() in ["true", "yes"]:
                    baseStruct = self.foamJson["dynamicMesh"]
                    for folder in baseStruct:
                        createDirSafely(folder)
                        for file in baseStruct[folder]:
                            copyFileSafely(os.path.join(
                                self.setupPath + baseStruct[folder][file]), os.path.join(folder, file))


entryPoint = sys.argv[1]

if entryPoint == "initFoam":
    projectStruct = loadJson('project.json')
    readmePath = findFile("READMEglobal.md", "tools")
    copyFileSafely(readmePath, "./README.md")
    for folder in projectStruct['foamFolders']:
        if not os.path.exists(folder):
            for element in foamStructure:
                newStudy = Study(element, folder)
                newStudy.create()
            os.system('git add .')
            os.system(
                'git commit -m "[%s] #INIT \'created project %s\'"' % (folder, folder))
        else:
            print("skipping project >" + folder + " since it already exists")
elif entryPoint == "newCase":
    currentCase = caseSelector()
    currentCase.create()
elif entryPoint == "initCase":
    currentCase = caseSelector()
    currentCase.initCase()
elif entryPoint == "symlinks":
    currentCase = caseSelector()
    currentCase.makeSymlinks()
elif entryPoint == "clone":
    currentCase = caseSelector()
    currentCase.clone()
elif entryPoint == "clear":
    currentCase = caseSelector()
    currentCase.clear()
elif entryPoint == "commit":
    currentCase = Case("run")
    currentCase.commitChanges()
elif entryPoint == "test":
    print("Nothing defined")
