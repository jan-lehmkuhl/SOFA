#!/usr/bin/env python3

#--------------------------------------------------------------------------#
# Contributor: Sebastian Tueck                                             #
# Last Change: February 01 2019                                            #
# Topic:       Process Handling                                            #
#--------------------------------------------------------------------------#

import subprocess
import os
import datetime
import sys


class procHandler(object):

    def __init__(self, nCores):
        self.nCores = nCores

    def general(self, cmd, text = None, logFilePath = None, wait = True):
            # wrapper around subprocess. takes a list of commands 
            # and excecutes them in bash while optionally
            # displaying a provided text and after excecution the 
            # duration of the process. If a path is specified the output
            # of the process will be redirected to that location.
            # Will also terminate the script if the process fails.
            #
            # Args:
            #   cmd:                list: commands to be excecuted
            #   text (opt.):        str: text to display while excecuting
            #   logFilePath (opt.): str: path where to redirect the output
            #
            # Return:
            #
            try:
                start = datetime.datetime.now()           
                if text:
                    self.printProcStart(text)
                if logFilePath:
                    if not os.path.exists(os.path.dirname(logFilePath)):
                        os.makedirs(os.path.dirname(logFilePath))
                    with open(logFilePath, 'w') as logfile:
                        proc = subprocess.Popen(cmd, stdout = logfile, stderr = subprocess.STDOUT)
                        if wait:
                            proc.wait()
                else:
                    with open(os.devnull, "w") as f:
                        proc = subprocess.Popen(cmd, stdout = f, stderr = subprocess.STDOUT)
                        if wait:
                            proc.wait()
                status = proc.returncode
                end = datetime.datetime.now()
                if wait:
                    assert(status == 0)
            except AssertionError:
                if text:
                    self.printProcFailed(text, (end-start))
                    # self.printFooterFailed()
                raise
                # sys.exit(0)
            else:          
                if text:
                    self.printProcEnd(text, (end-start))
                    

    def foam(self, process, option = None, serial = False):
        # wrapper of processHandler for openFoam processes 
        #
        # Args:
        #   process:        str:openFoam programm
        #   option (opt.):  str:option for programm 
        #   serial (opt.):  bool: overwrite parallel running
        #
        # Return:
        #
        text = str("Excecuting " + process)
        logFilePath = str("log/" + process + ".log")
        if self.nCores == 1 or serial:
            if option:
                cmd = [process, option]
            else:
                cmd = [process]
        else:
            if option:
                cmd = ["mpirun", "-np", str(self.nCores), process, option, "-parallel"]
            else:
                cmd = ["mpirun", "-np", str(self.nCores), process, "-parallel"]
        self.general(cmd, text, logFilePath)

    ###########################################################################
    # graphical output
    ###########################################################################

    def printFooterFailed(self):
        # prints footer for failed meshing process
        #
        # Args:
        #
        # Return:
        #
        print("\n==========================================================================")
        print("Procedure failed")
        print("==========================================================================")

    def printProcStart(self, text):
        # prints formated text during excecution. Next output
        # will overwrite this
        #
        # Args:
        #   text:   str: text to be displayed during excecution
        #
        # Return:
        #
        sys.stdout.write(" - {0:<30s}\r".format(text))

    def printProcEnd(self, text, duration):
        # prints formated text after excecution
        #
        # Args:
        #   text:       str: text to be displayed during excecution
        #   duration:   str: excecution time
        #
        # Return:
        #
        sys.stdout.flush()
        sys.stdout.write(" - {0:<30s} --> finished after {1:25s}\n".format(text, str(duration)))

    def printProcFailed(self, text, duration):
        # prints formated text after failure
        #
        # Args:
        #   text:       str: text to be displayed during excecution
        #   duration:   str: excecution time
        #
        # Return:
        #
        sys.stdout.flush()
        sys.stdout.write(" - {0:<30s} --> failed after {1:25s}\n".format(text, str(duration)))
