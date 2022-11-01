#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Sebastian Tueck                                             #
# Last Change: February 01 2019                                            #
# Topic:       File handling                                               #
#--------------------------------------------------------------------------#

import os
import json
import collections



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
            # if verbose:     print(  "    load json:              ", jsonPath)  
            jsonStr = jsonFile.read()
            jsonStr = re.sub( " // .*", "", jsonStr, flags=re.MULTILINE )
            jsonStr = re.sub( "\n",     "", jsonStr, flags=re.MULTILINE )
            jsonPy = json.loads( jsonStr, object_pairs_hook=collections.OrderedDict )
            return(jsonPy)
    else:
        raise SystemExit("ERROR missing json file: " +jsonPath)
