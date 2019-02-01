#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Sebastian Tueck                                             #
# Last Change: February 01 2019                                            #
# Topic:       Meshing process                                             #
#--------------------------------------------------------------------------#

import os
import sys

from procHandling import procHandler


class foamCAD(object):
    # class for openFoam cad procedures

    def __init__(self):
        self.procHandler = procHandler(1)

    def cleanVTK(self):
        for fileName in os.listdir("vtk"):
            if os.path.splitext(fileName)[1] == ".vtk":
                print("Processing >%s<" % fileName)
                bad_words = ['METADATA', 'INFORMATION ', 'NAME ', "DATA "]
                with open(os.path.join("vtk", fileName)) as oldfile, open(os.path.join("vtk", "Clean_" + fileName), 'w') as newfile:
                    for line in oldfile:
                        if not any(line.startswith(bad_word) for bad_word in bad_words):
                            newfile.write(line)

    def combineSTL(self):
        fileNames = []
        for fileName in os.listdir("stl"):
            if os.path.splitext(fileName)[1] == ".stl":
                fileNames.append(fileName)
        print(fileNames)
        with open('stl/regionSTL.stl', 'w') as outfile:
            for fname in fileNames:
                print("Processing >%s<" %fname)
                with open(os.path.join("stl", fname)) as infile:
                    for line in infile:
                        outfile.write(line)

    def checkSurface(self):
        for fileName in os.listdir("stl"):
            if os.path.splitext(fileName)[1] == ".stl":
                self.procHandler.general(["surfaceCheck", os.path.join(
                    "stl", fileName)], "Checking " + fileName, os.path.join("log", os.path.splitext(fileName)[0] + ".log"))
    
    def view(self):
            self.procHandler.general(["paraview"], wait = False)
        
###################################################################
# Main Programm
###################################################################
entryPoint = sys.argv[1]
cad = foamCAD()

if entryPoint == "checkSurfaces":
    cad.checkSurface()
if entryPoint == "cleanVTK":
    cad.cleanVTK()
if entryPoint == "combineSTL":
    cad.combineSTL()
if entryPoint == "view":
    cad.view()
