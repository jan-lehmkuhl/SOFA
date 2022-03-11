#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Jan Lehmkuhl                                                #
# Topic:       test for clean files                                        #
#--------------------------------------------------------------------------#


import os
import sys
import argparse



###############################################################################
#   MAIN PROGRAMM
###############################################################################

# read arguments and options from command line
parser = argparse.ArgumentParser(description='SOMEDESCRIPTION')
parser.add_argument( 'file',  help="SOMEHELP" )
args = parser.parse_args()      # stores all parsed arguments to args

isGitChanged = os.system("git diff --quiet " +args.file)
if not isGitChanged == 0:   # zero means clean
    print("git changes in:      " +args.file)
    print(os.system("git --no-pager diff " +args.file +" | tee --append diff.txt"))
    sys.exit(1)
else:
    print("no git changes in:   " +args.file)
