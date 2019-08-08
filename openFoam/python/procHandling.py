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

    def nextLogFile(self, path, ident):
        # finds the next name for a log file
        #
        # Args :
        #   path:   path to folder to look in
        #   ident:  identifiert for type of logfile ("snappyHexMesh")
        #
        # Return :
        #   nextFile    name of the next log file
        #
        nChar = len(ident)
        maxNo = 0

        # find all files which match ident and have the ending .log
        subFiles = [f.name for f in os.scandir(path) if f.is_file()]
        for fileName in subFiles:
            if (fileName[:nChar] == ident and fileName[-4:] == ".log"):
                currentNo = fileName[len(ident):-4]
                if not currentNo.isdigit():
                    currentNo = 0
                currentNo = int(currentNo)
                if currentNo > maxNo:
                    maxNo = currentNo

        nextFile = ident+str(maxNo+1)+".log"
        return(nextFile)

    def combineLogFiles(self, path, ident):
        # lists all files matching "ident" and write them into a single file
        # in order of modification date
        #
        # Args :
        #   path:   path to folder to look in
        #   ident:  identifiert for type of logfile ("snappyHexMesh")
        #
        # Return :
        #   sideEffect:    writes out new logfile
        #
        nChar = len(ident)
        files = []
        # find all files which match ident and have the ending .log
        subFiles = [f.name for f in os.scandir(path) if f.is_file()]
        for fileName in subFiles:
            if (fileName[:nChar] == ident and fileName[-4:] == ".log"):
                files.append(fileName)

        if len(files) > 1:
            # add path to each file
            files = [os.path.join(path, f) for f in files]
            files.sort(key=lambda x: os.path.getmtime(x))

            # combine all files into one
            with open(path+"/"+ident+"_combined.log", 'w') as outfile:
                for fileName in files:
                    with open(fileName) as infile:
                        for line in infile:
                            if line.strip():
                                outfile.write(line)

    def general(self, cmd, text=None, logFilePath=None, wait=True):
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
                    proc = subprocess.Popen(
                        cmd, stdout=logfile, stderr=subprocess.STDOUT)
                    if wait:
                        proc.wait()
            else:
                with open(os.devnull, "w") as f:
                    proc = subprocess.Popen(
                        cmd, stdout=f, stderr=subprocess.STDOUT)
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

    def foam(self, process, option=None, serial=False):
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
        if not os.path.exists("./log"):
            os.makedirs("./log")
        logFile = self.nextLogFile("./log", str(process))
        logFilePath = str("log/" + logFile)
        if self.nCores == 1 or serial:
            if option:
                cmd = [process, option]
            else:
                cmd = [process]
        else:
            if option:
                cmd = ["mpirun", "-np",
                       str(self.nCores), process, option, "-parallel"]
            else:
                cmd = ["mpirun", "-np", str(self.nCores), process, "-parallel"]
        self.general(cmd, text, logFilePath)
        self.combineLogFiles("./log", str(process))

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
        print(
            "\n==========================================================================")
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
        sys.stdout.write(
            " - {0:<30s} --> finished after {1:25s}\n".format(text, str(duration)))

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
        sys.stdout.write(
            " - {0:<30s} --> failed after {1:25s}\n".format(text, str(duration)))
