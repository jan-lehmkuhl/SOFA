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


def convertToRelativePath( absolutePath, referencePath ,verbose=False):
    if referencePath and absolutePath.startswith( referencePath ):
        return absolutePath[len(referencePath):]
    else: 
        if verbose:
            print(  "cannot create relative path from: ", absolutePath, " for Reference: ", referencePath )
        return absolutePath

def createDirSafely(dst, debugRefPath=None):
    # creates a directory recursively if it doesn't exist
    #
    # Args:
    #   dst:   the path to the directory
    #
    # Return:
    #   side effects
    #
    # FIXME add warning for relative path
    dstShort = convertToRelativePath( dst, debugRefPath )
    if not os.path.isdir(dst):
        print("Creating folder     ", dstShort )
        os.makedirs(dst)
    else:
        print("Skip existing folder     ", dstShort )

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



def createSymlinkSavely(src, dst, referencePath=None, verbose=False ):
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
        srcShort = convertToRelativePath( src, referencePath )
        dstShort = convertToRelativePath( dst, referencePath )
        if os.path.islink(dst):
            if not os.readlink(dst) == relSrc:
                print("Overwriting link     %s \t\t with pointer to   %s" % (dstShort, srcShort))
                os.remove(dst)
                os.symlink(relSrc, dst)
            else:
                if verbose: print("Skip correct link    %s \t\t with pointer to   %s" % (dstShort, srcShort))
        elif not os.path.exists(dst):
            print("Creating link to     %s \t\t with pointer to   %s" % (dstShort, srcShort))
            os.symlink(relSrc, dst)
        else:
            print("Unabel to create target >%s< since it exists" % dst)
    else:
        print("Unabel to find >%s<" % src)

def copyFileSafely(src, dst, referencePath=None, verbose=False ):
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
                srcShort = convertToRelativePath( src, referencePath, verbose )
                dstShort = convertToRelativePath( dst, referencePath, verbose )
                if not os.path.exists(dst):
                    print("Copying file to      %s \t from %s" % (dstShort, srcShort))
                    shutil.copyfile(src, dst)
                else:
                    print("Skip existing file       ", dstShort )
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

def loadJson(jsonPath, verbose=False):
    # Loads a passed .json file if it exists
    #
    # Args:
    #   jsonPath:   s: the path to a Json file
    #
    # Return:
    #   jsonPy:     d: parsed json
    #
    import sys 
    import re

    if os.path.exists(jsonPath):
        with open(jsonPath, 'r') as jsonFile:
            if verbose:     print(  "    load json:              ", jsonPath)
            jsonStr = jsonFile.read()
            jsonStr = re.sub( " // .*", "", jsonStr, flags=re.MULTILINE )
            jsonStr = re.sub( "\n",     "", jsonStr, flags=re.MULTILINE )
            jsonPy = json.loads( jsonStr, object_pairs_hook=collections.OrderedDict )
            return(jsonPy)
    else:
        print(" ")
        print("ERROR: json file >%s< does not exist" % jsonPath)
        print("    current directory is: " +os.getcwd() +"\n")
        sys.exit(1)


def handleStudyStructFolder( studyStructHome, fileAttributes, targetFolder, verbose=False, debugRefPath=None ):
    createDirSafely( os.path.join( targetFolder, fileAttributes['relPath'] ), debugRefPath=debugRefPath )
    if fileAttributes['createGitKeep']:
        pass    # TODO create .gitkeep

def handleStudyStructFile( studyStructHome, fileAttributes, targetFolder, verbose=False, debugRefPath=None ):
    source = os.path.join( studyStructHome, fileAttributes['sourcePath'] ) 
    target = os.path.join( targetFolder   , fileAttributes['targetPath'] ) 

    if fileAttributes['isSymlink']: 
        createSymlinkSavely( source, target, referencePath=debugRefPath, verbose=verbose )
        os.system("git add " +target)
    else:
        copyFileSafely( source, target, referencePath=debugRefPath, verbose=verbose )
        os.system("git add " +target)
    pass


def hasRepositoryStagedFiles(  ):
    var = os.system( "git diff --cached --quiet" )
    # print("var: ", var)
    if var == 0: 
        return False
    else:
        return True
