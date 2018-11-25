#!/usr/bin/python

import os
import time

# os.system("clear")

def createDirSafely( directory ):
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print( "folder >" + directory + "< already exists" )    


createDirSafely( "test-folder-foam-2/tut" )
