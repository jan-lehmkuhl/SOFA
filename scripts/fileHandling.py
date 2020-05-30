#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Sebastian Tueck                                             #
# Last Change: February 01 2019                                            #
# Topic:       File handling                                               #
#--------------------------------------------------------------------------#

import os
import shutil
import json
import errno
import collections


def findFile(fileName, turnFolder):
    # FIXME move to separate
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
        print("Could not find >%s< in subfolders of >%s<" % (fileName, turnFolder) )
        return(False)


def createDirSafely(dst):
    # creates a directory recursively if it doesn't exist
    #
    # Args:
    #   dst:   the path to the directory
    #
    # Return:
    #   side effects
    #
    # FIXME add warning for relative path
    if not os.path.isdir(dst):
        os.makedirs(dst)
        print("Creating folder     %s " %dst )
    else:
        print("Skipping >%s< since it already exists" % dst)

def createDir(dst):
    # creates a directory recursively if it doesn't exist
    #
    # Args:
    #   dst:   the path to the directory
    #
    # Return:
    #   side effects
    #
    if not os.path.exists(dst):
        try:
            os.makedirs(dst, 0o700)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise



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
            print("Creating link to    %s \t\t from %s" % (dst, src))
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
    if os.path.islink(src):
        linkTo = os.readlink(src)
        createSymlinkSavely(linkTo, dst)
    else:
        if os.path.exists(src):
            if not os.path.isdir(src):
                if not os.path.exists(dst):
                    print("Copying file to     %s \t from %s" % (dst, src))
                    shutil.copyfile(src, dst)
                else:
                    print("Skipping >%s< since it already exists" % src)
            else:
                print("Skipping >%s< because it is a directory" % src)
        else:
            print("Unabel to find >%s<" % src)

def copyFile(src, dst):
    try:
        assert(os.path.exists(dst))
        shutil.copyfile(src, dst)
    except FileNotFoundError:
        print("Unabel to find >%s<" % src)
        raise
    except IsADirectoryError:
        print("Either >%s< or >%s< is a directory" % (src, dst))
        raise
    except AssertionError:
        print("Skipping >%s< since it already exists" % src)
        raise
    else:
        print("Copying file from >%s< to >%s<" % (src, dst))

def copyFolderSafely(src, dst):
    # copies a file if it exists
    #
    # Args:
    #   src:   s: path to the file to be copied
    #   dst:   s: path to copy the file to
    #
    # Return:
    #   side effects
    #
    if os.path.islink(src):
        linkTo = os.readlink(src)
        createSymlinkSavely(linkTo, dst)
    else:
        if os.path.exists(src):
            if not os.path.isfile(src):
                if not os.path.exists(dst):
                    shutil.copytree(src, dst,symlinks=True)
                    print("Copying folder from >%s< to >%s<" % (src, dst))
                else:
                    print("Skipping >%s< since it already exists" % src)
            else:
                print("Skipping >%s< because it is a file" % src)
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
    import sys 
    
    if os.path.exists(jsonPath):
        with open(jsonPath, 'r') as jsonFile:
            jsonPy = json.load(jsonFile, object_pairs_hook=collections.OrderedDict)
            return(jsonPy)
    else:
        print(" ")
        print("ERROR: json file >%s< does not exist" % jsonPath)
        print("    current directory is: " +os.getcwd() +"\n")
        sys.exit("TERMINATE python script")


def handleStudyStructFolder( studyStructHome, fileAttributes, targetFolder, verbose=False ):
    createDirSafely( os.path.join( targetFolder, fileAttributes['relPath'] ) )
    if fileAttributes['createGitKeep']:
        pass    # TODO create .gitkeep

def handleStudyStructFile( studyStructHome, fileAttributes, targetFolder, verbose=False ):
    source = studyStructHome  +"/"   +fileAttributes['sourcePath']
    target = targetFolder     +"/"   +fileAttributes['targetPath']

    if fileAttributes['isSymlink']: 
        createSymlinkSavely(source,target)
    else:
        copyFileSafely(source,target)

