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
import fnmatch
import subprocess
import shutil

# add paths
file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, file_path ) 

from fileHandling import createDirSafely
from fileHandling import createSymlinkSavely
from fileHandling import copyFileSafely
from fileHandling import copyFolderSafely
from fileHandling import loadJson
from fileHandling import findFile
from folderHandling import findFolder
from folderHandling import findParentFolder



def cfdAspectSelector(path=None, verbose=False):
    # determines the aspectType of the case from the name of the containing folder
    #
    # Args:
    #   path:       s: path to pass
    #
    # Return:
    #   aspectName:  s: Name of the containing folder stripped of numbers
    #               this should equal the aspectType
    #
    from aspect import readFoamStructure

    if path is None:
        path = "./"
        caseFolder = os.path.basename(os.getcwd())
    else:
        caseFolder = os.path.basename(path)
    aspectName = ''.join(
        [i for i in caseFolder if not i.isdigit()])  # remove digits
    if aspectName in readFoamStructure():
        if aspectName == "cad":
            return(CadCase(path=path,verbose=verbose))
        elif aspectName == "mesh":
            return(MeshCase(path=path,verbose=verbose))
        elif aspectName == "run":
            return(RunCase(path=path,verbose=verbose))
        elif aspectName == "survey":
            return(SurveyCase(path=path,verbose=verbose))
    else:
        print("Unknown aspect >%s< in caseFolder: >%s<" % (aspectName, caseFolder) )
        return(False)


class Case(object):
    # base class to handle all operations related to cases

    def __init__(self, storagePath=None, aspectType=None, caseStructure=None, verbose=False, path="./"):
        from aspect import readFoamStructure
        from study import StudyStructure
        import fnmatch

        # store known values to self
        # ================================================================================
        self.className4 = "Case"    # only for debugging purpose
        self.aspectRoot = storagePath
        self.aspectType = aspectType
        self.verbose    = verbose
        if self.verbose:
            print("start case constructor")
        currentDir  = os.path.basename( os.getcwd() )

        # search for sofa environment provided information
        # ================================================================================
        # project handling
        self.projectRoot    = findParentFolder( "project.json" )
        if caseStructure == None :
            self.studyRoot      = findParentFolder( "sofa.study.json", verbose=verbose )
            thisStudyStructure  = StudyStructure( studyJsonFolder=self.studyRoot ) 
            self.studyName = os.path.basename(self.studyRoot)
        # aspect handling
        if self.aspectType == None: 
            # read Case.aspectType from foldername
            if currentDir in thisStudyStructure.aspectList:
                self.aspectType     = currentDir
                self.aspectRoot     = os.getcwd()
        # case handling
        if 'thisStudyStructure' in locals():
            if currentDir[:-3] in thisStudyStructure.aspectList:
                self.aspectType     = currentDir[:-3]
                self.path           = os.getcwd()
                self.caseName       = currentDir
                if self.aspectRoot == None :
                    self.aspectRoot = os.path.abspath(os.path.join(self.path, os.pardir))
        if self.aspectType == None: 
            sys.exit(1)

        if caseStructure == None :
            self.structure      = thisStudyStructure.aspectList[self.aspectType]['case000']
        else:
            self.structure      = caseStructure

        if 'caseName' not in self.__dict__: 
            self.createNew  = True
            self.caseName   = self.nextCaseName( self.aspectRoot )
            self.path       = os.path.join( self.aspectRoot, self.caseName )
        else:
            self.createNew  = False
            for file in os.listdir( self.path ):
                if fnmatch.fnmatch(file, "sofa."+ self.aspectType +"*.json"):
                    if self.verbose: 
                        print("with case-json:   "+ file+ "\tin: "+ self.path )
                    self.pathToJson = os.path.join(self.path, file)


        # store linked cases to self
        # ================================================================================
        self.caseJson = None
        self.linkedCase = None
        self.linkedReport = None
        self.pathToLinkedCase = None
        self.pathToLinkedReport = None
        self.symlinksClean = False
        if os.path.exists(self.path):
            # load case .json 
            self.caseJson = loadJson(self.pathToJson)
            # extract linked cases from case.json according to foamStructure gen in project.json
            foamStructure   = readFoamStructure()
            if 'linkName' in foamStructure[self.aspectType]: 
                self.linkedCase = self.caseJson["buildSettings"][foamStructure[self.aspectType]["linkName"]]
            if self.linkedCase:
                # differentiate between single links and a list of links (survey)
                if isinstance(self.linkedCase, str):
                    self.pathToLinkedCase = findFolder( self.linkedCase
                                                      , foamStructure[ foamStructure[self.aspectType]["linkType"] ]["aspectName"] )
                elif isinstance(self.linkedCase, list):
                    self.pathToLinkedCase = []
                    for element in self.linkedCase:
                        self.pathToLinkedCase.append(findFolder( element
                                                               , foamStructure[ foamStructure[self.aspectType]["linkType"] ]["aspectName"] ) )
                else:
                    print(
                        "Unexpected aspectType of self.linkPath in __init__ of %s" % self.name)
        pass  # end linked cases search


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
        charCount = len(self.aspectType)
        for folder in subfolders:
            if folder[:charCount] == self.aspectType:
                currentNo = int(folder[charCount:])
                if currentNo > maxNo:
                    maxNo = currentNo
        CaseName = str(self.aspectType + format(maxNo + 1, "0>3d"))
        return(CaseName)


    def getStudyName(self):
        # finds the projectname of a case
        #
        # Args:
        #
        # Return:
        #   name:   name of the next case folder
        #
        from aspect import readFoamStructure
        foamStructure   = readFoamStructure()

        i = 0
        wd = os.getcwd()
        subdirs = os.listdir(os.getcwd())
        while i < 5:
            if foamStructure["cad"]["aspectName"] in subdirs:
                return(os.path.basename(os.path.normpath(wd)))
            else:
                wd = os.path.join(wd, os.path.pardir)
                subdirs = os.listdir(wd)
                i += 1
        else:
            print("Could not find project name")
            return(False)


    def create(self):
        # create a new case inside a Aspect depending on the aspectType of case
        #
        # Args:
        #
        # Return:
        #   side effects
        #
        from fileHandling import handleStudyStructFile
        from fileHandling import handleStudyStructFolder
        if self.verbose:    print(  "creating case:         \t\t  >>  " +self.caseName +"  <<")

        # create case folder
        self.casePath = os.path.join( self.aspectRoot, self.caseName ) 
        createDirSafely( self.casePath, debugRefPath=self.projectRoot )

        # create caseXXX content
        if 'folders' in self.structure : 
            for thisFolder in self.structure['folders'] : 
                handleStudyStructFolder( self.structure['localpath'], thisFolder, self.casePath, self.verbose, debugRefPath=self.projectRoot ) 
        if 'files' in self.structure : 
            for thisFile in self.structure['files'] : 
                if 'onlyAtCaseCreation' in thisFile: 
                    if thisFile['onlyAtCaseCreation'] and not self.createNew : 
                        if self.verbose: 
                            print("Skip onlyAtCreation file: "+ thisFile['targetPath'])
                        continue
                handleStudyStructFile( self.structure['localpath'], thisFile, self.casePath, self.verbose, debugRefPath=self.projectRoot ) 
        if 'caseLinks' in self.structure : 
            for thisFile in self.structure['caseLinks'] : 
                createSymlinkSavely(  os.path.join(self.casePath, thisFile['sourcePath'])
                                    , os.path.join(self.casePath, thisFile['targetPath']) , referencePath=self.casePath, verbose=self.verbose)
        return(True)


    def createUpstreamAspectLinks(self):
        from fileHandling import createSymlinkSavely
        if self.verbose:    print(  "create upstream aspect links for:  \t  >>  " +self.caseName +"  <<")

        # create upstreamAspectLink
        if 'upstreamAspects' in self.structure : 
            for thisUpstreamConnection in self.structure['upstreamAspects'] : 
                # sort information
                thisUpstreamAspect  = thisUpstreamConnection['upstreamAspect']
                upstreamCase        = self.caseJson[ thisUpstreamConnection['caseJsonKey'][0] ][ thisUpstreamConnection['caseJsonKey'][1] ]     # TODO read for free key depth
                upstreamTarget      = os.path.join('..','..',thisUpstreamAspect,upstreamCase)

                if thisUpstreamConnection['createDirectSymlink']: 
                    createSymlinkSavely(upstreamTarget,upstreamCase,verbose=self.verbose)

                if 'specialLinks' in thisUpstreamConnection : 
                    for thisLink in thisUpstreamConnection['specialLinks'] : 
                        # define src/dst
                        if thisUpstreamConnection['useCaseJsonWithoutAspect']:
                            src         = os.path.join( '..','..',upstreamCase, thisLink['upstreamCasePath'] )
                        else:
                            if thisLink['upstreamCasePath'] =="":
                                src     = upstreamTarget
                            else: 
                                src     = os.path.join( upstreamTarget, thisLink['upstreamCasePath'] )
                        dst = thisLink['targetPath']

                        # create file
                        if thisLink['separateFiles']:
                            for element in os.listdir(src):
                                if thisLink['copyFile']: 
                                    copyFileSafely( os.path.join(src,element), os.path.join(dst,element), overwrite=True, verbose=self.verbose )
                                else:
                                    createSymlinkSavely( os.path.join(src,element), os.path.join(dst,element), verbose=self.verbose )
                        else:
                            if thisLink['copyFile']: 
                                copyFileSafely( src, dst, overwrite=True, verbose=self.verbose )
                            else:
                                createSymlinkSavely( src, dst, verbose=self.verbose )
        return(True)


    def clone(self):
        # create a clone of the current case
        #
        # Args:
        #
        # Return:
        #   side effects: makes a clone of the case
        #
        currentCase = self.path
        caseName = self.nextCaseName(os.pardir)
        clonePath = os.path.join(os.pardir, caseName)
        while True:
            print("Clone case from >%s< to >%s< ? (Y/n)" % (currentCase, caseName))
            answer1 = input().lower()
            if answer1 in ["y", "yes",""]:
                while True:
                    print("Include results? (y/N)")
                    answer2 = input().lower()
                    if answer2 in ["y", "yes"]:
                        print("Cloning complete case >%s< to >%s<" % (currentCase, caseName))
                        shutil.copytree(os.path.join(os.pardir, currentCase),
                                        clonePath, symlinks=True)
                        break
                    if answer2 in ["n", "no",""]:
                        print("Cloning case >%s< to >%s< without results" % (currentCase, caseName))
                        os.makedirs(clonePath)
                        for name in os.listdir("."):
                            if fnmatch.fnmatch(name, "[1-9]*") or fnmatch.fnmatch(name, "[0-9].[0-9]*"):
                                continue
                            elif fnmatch.fnmatch(name, "processor*"):
                                createDirSafely(os.path.join(clonePath,name))
                                for subDir in os.listdir(os.path.join("./", name)):
                                    if fnmatch.fnmatch(subDir, "[1-9]*") or fnmatch.fnmatch(subDir, "[0-9].[0-9]*"):
                                        continue
                                    else:
                                        copyFolderSafely(os.path.join(name, subDir), os.path.join(clonePath,name,subDir))
                                continue
                            elif fnmatch.fnmatch(name, "postProcessing*"):
                                continue
                            elif fnmatch.fnmatch(name, "log*"):
                                continue
                            elif os.path.isfile(name):
                                copyFileSafely(name,os.path.join(clonePath,name))
                                continue
                            else:
                                copyFolderSafely(name,os.path.join(clonePath,name))
                        break
                while True:
                    # git handling
                    os.system('git add %s' % clonePath)
                    message = '[%s %s] #CLONE from >%s<' % (self.studyName, caseName, os.path.basename(currentCase))
                    print("staged commit for %s with commit-message: \n\t%s" % (caseName, message) )
                    print("\nCommit cloning of >%s< to >%s< ? (y/N)" % (os.path.basename(currentCase), caseName))
                    answer3 = input().lower()
                    if answer3 in ["y", "yes"]:
                        os.system('git commit -m "%s"' % message)
                        break
                    elif answer3 in ["n", "no",""]:
                        break
                    pass
                break
            if answer1 in ["n", "no"]:
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
                        studyName = self.getStudyName()
                        os.system('git add .')
                        os.system('git commit -m "[%s%s] #CLEAR \'cleared case >%s< in project >%s<\'"' 
                                  % (studyName, caseName.capitalize(), caseName, studyName))
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
        from aspect import readFoamStructure

        if self.verbose:    print("start removing symlinks")
        extensions = [".stl", ".vtk"]
        folder = ["polyMesh", "cadPics", "meshPics",
                  "drafts", "meshReport", "layerSizing"]
        foamStructure   = readFoamStructure()
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
        if self.verbose:    print("end removing symlinks")


    def commitInit(self):
        # asks user if he wants to commit the initialisation to git
        #
        # Args:
        #
        # Result:
        #   side effects:   commits changes of case
        #
        studyName = self.getStudyName()
        caseName = os.path.basename(os.getcwd())
        while True:
            print("Commit initialisation of %s ? (y/n)" % caseName)
            answer = input()
            answer = answer.lower()
            if answer in ["y", "yes"]:
                studyName = self.getStudyName()
                os.system('git add .')
                os.system('git commit -m "[%s%s] #INIT \'initialised case >%s< in project >%s<\'"' % (
                    studyName, caseName.capitalize(), caseName, studyName))
                break
            elif answer in ["n", "no"]:
                break


    def updateJson(self):
        # update json file of a case with newest version from tools
        #
        # Args:
        #
        # Result:
        #   side effects:   overwrite current .json
        #

        # find and load most recent version of json from framework
        newJsonPath = findFile(self.aspectType + ".json", "tools")
        newJson = loadJson(newJsonPath)
        # check if present
        if newJsonPath:
            # loop first level of keys 
            for key1 in self.caseJson:
                # if found element is a string assign value
                if isinstance(self.caseJson[key1], str):
                    newJson[key1] = self.caseJson[key1]
                # if found element is a dict iterate
                elif isinstance(self.caseJson[key1], dict):
                    # assign value 
                    for key2 in self.caseJson[key1]:
                        newJson[key1][key2] = self.caseJson[key1][key2]
        else:
            print("No version of %s found in framework" %str(self.aspectType + ".json"))
        # save new Json file over old file
        with open(os.path.join(self.path, self.aspectType + ".json"), 'w') as outfile:
            json.dump(newJson, outfile, indent=4)


#TODO remove specialized classes
class CadCase(Case):
    # Specialized class for cad cases, which inherits from the base Case class

    def __init__(self, path="./", verbose=False):
        # execute init of parent class
        super().__init__(aspectType="cad", path=path, verbose=verbose)
        self.name = "CadCase"   # only for debugging purpose


    def makeSymlinks(self):
        print("Cases of aspectType >cad< do not support option symlinks")


class MeshCase(Case):
     # Specialized class for cad cases, which inherits from the base Case class

    def __init__(self, path="./", verbose=False):
        super().__init__(aspectType="mesh", path=path, verbose=verbose)
        self.name = "MeshCase"
        self.Builder = foamBuilder()

    def makeSymlinks(self):
        # specialized method to create all symlinks needed for a case
        # of aspectType mesh
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
            createDirSafely( os.path.join( self.pathToLinkedCase, "doc" ) )
            createDirSafely( os.path.join( self.pathToLinkedCase, "stl" ) )
            createDirSafely( os.path.join( self.pathToLinkedCase, "vtk" ) )
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
            self.copyReport(run=False)
            if not linkedGeometry:
                print("WARNING: Did not link to any geometry files")
            return(True)


class RunCase(Case):
    # Class for run cases

    def __init__(self, path=None, verbose=False):
        super().__init__(aspectType="run", path=path, verbose=verbose)
        self.name = "RunCase"
        if self.caseJson:
            self.Builder = foamBuilder(self.caseJson["buildSettings"])

    def makeSymlinks(self):
        # specialized method to create all symlinks needed for a case
        # of aspectType run
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
            createSymlinkSavely(  os.path.join( self.pathToLinkedCase, "constant/polyMesh")
                                , os.path.join( "./constant/polyMesh" ))
            createDirSafely( os.path.join( self.pathToLinkedCase, "doc") )
            for element in os.listdir(os.path.join(self.pathToLinkedCase, "doc")):
                currentPath = os.path.join(
                    self.pathToLinkedCase, "doc", element)
                createSymlinkSavely(currentPath, os.path.join("doc", element))
            self.copyReport(run=False)
            return(True)

    def initCase(self):
        # specialised method to initialise a case of aspectType run
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

class SurveyCase(Case):
    # Class for survey cases

    def __init__(self, path=None, verbose=False):
        super().__init__(aspectType="survey", path=path, verbose=verbose)
        self.name = "surveyCase"

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

