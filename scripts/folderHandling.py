#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Jan Lehmkuhl                                                #
# Topic:       do SOFA-project stuff                                       #
#--------------------------------------------------------------------------#


# import libraries
# -------------------------------------------------------------------
# import librarys
# import json
import os
import sys
# import shutil
# import fnmatch
# import subprocess
# import argparse


# add additional path for import
# -------------------------------------------------------------------
# sys.path.insert(1, './tools/framework/openFoam/python') 


# load functions
# -------------------------------------------------------------------
# from fileHandling import createDirSafely
# from fileHandling import createSymlinkSavely
# from fileHandling import copyFileSafely
# from fileHandling import copyFolderSafely
# from fileHandling import loadJson



def walklevel(some_dir, level=-1, followlinks=False):
    # https://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
    #   level=-1 walks through all files (os.walk default)
    #   level=0 lists only the current directory files 
    #   level=1 finds lists all files in the first level subfolder 
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir, followlinks=followlinks):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if ( num_sep + level <= num_sep_this ) and ( level != -1 ): 
            # deletes next walking through dirs if to much seperaters
            del dirs[:]


def findChildFolders( containingFile, startFolder=os.getcwd(), directoryMaxDepth=-1 , allowSymlinks=False, relativeOutput=False):
    folderList = []
    for subdir, dirs, files in walklevel( startFolder, directoryMaxDepth , followlinks=allowSymlinks):
        for file in files:
            if file == containingFile :
                if relativeOutput and subdir.startswith(startFolder+"/") :
                    subdir = subdir[len(startFolder+"/"):]
                else:
                    print("WARNING intended relative childFolder return is not converted to relative: " +subdir )
                folderList.append( subdir )
    if folderList == [] :
        print(  "ERROR: no SubFolders with >" +containingFile +"< inside in: " +startFolder +"\n") 
    folderList = sorted(folderList, key=str.lower)
    return folderList


def findParentFolder( containingFile, startFolder=os.getcwd(), allowFail=False, verbose=False ):
    wd = startFolder
    subdirs = os.listdir(os.getcwd())
    i = 0
    while i < 4:
        if containingFile in subdirs:
            return wd
        else:
            wd = os.path.join(wd, os.path.pardir)
            wd = os.path.abspath( wd )
            subdirs = os.listdir(wd)
            i += 1
    else:
        if verbose or not allowFail: 
            print("WARNING Could not find:  >", containingFile, "< in parent folders from: ", startFolder )
        if allowFail: 
            return None
        else:
            sys.exit(0)


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

