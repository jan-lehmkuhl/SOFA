#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Sebastian Tueck, Jan Lehmkuhl                               #
# Last Change: February 01 2019                                            #
# Topic:       Project builder                                             #
#--------------------------------------------------------------------------#

import os
import sys
import argparse

import subprocess


# add paths
file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, file_path ) 
sys.path.insert(1, os.path.realpath( file_path +'/../../../scripts' ) ) 

from case import Case



###############################################################################
# MAIN PROGRAMM
###############################################################################

# read arguments and options from command line
parser = argparse.ArgumentParser(description='input for reports.py')
parser.add_argument( '--verbose', '-v', action="store_true", dest="verbose", default=False )

# store all parsed arguments to args
args = parser.parse_args()

# verbose output
if args.verbose :   print("starting report.py in verbose mode" )
if args.verbose :   print("    in folder (os.getcwd):   " + os.getcwd() )
if args.verbose :   print("    with report.py in:       " + file_path )


# default part
if True: 
    print("Start create case report")
    thisCase = Case( verbose=parser.parse_args().verbose )

    # search for report destination
    reportDst = None
    if 'upstreamAspects' in thisCase.structure : 
        for thisUpstreamConnection in thisCase.structure['upstreamAspects'] : 
            if "report" in thisUpstreamConnection['upstreamAspect']: 
                if 'specialLinks' in thisUpstreamConnection : 
                    for thisLink in thisUpstreamConnection['specialLinks'] : 
                        reportDst = thisLink['targetPath']

    # execute R report
    if reportDst == None:
        print("no report defined")
    else: 
        cmd = ['R', '-e' , 'rmarkdown::render(\'' + reportDst + '\')']
        #logFilePath = os.path.join("log",str("runReport" + ".log"))
        runReport = subprocess.Popen(cmd)# , logFilePath)  
        runReport.wait()
    pass
