#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Jan Lehmkuhl                                                #
# Topic:       test for clean files                                        #
#--------------------------------------------------------------------------#


import os
import argparse
import subprocess



###############################################################################
#   MAIN PROGRAMM
###############################################################################

# read arguments and options from command line
parser = argparse.ArgumentParser(description='SOMEDESCRIPTION')
parser.add_argument( 'file',  help="SOMEHELP" )
args = parser.parse_args()      # stores all parsed arguments to args

isGitChanged = os.system("git diff --quiet " +args.file)
if not isGitChanged == 0:   # zero means clean
    print("ERROR git changes in: " +args.file)
    gitDiff = subprocess. getoutput("git diff " +args.file)
    print (gitDiff)
    if os.path.isfile("debug-mode"):
        with open ('debug-mode', 'a') as f: f.write ("git changes in: " +args.file +"\n")
    else:
        raise SystemExit("ERROR raise SystemExit: git changes in:   " +args.file)
else:
    print("no git changes in:   " +args.file)
