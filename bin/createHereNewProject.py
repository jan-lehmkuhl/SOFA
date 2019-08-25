#!/usr/bin/env python3

import os
import shutil


#################################################
# init repository
#################################################

os.system("git init")
os.system("git submodule add git@gitlab.com:schlupp/simulation-projects.git tools/framework ")


#################################################
# copy first files
#################################################

dirpath = os.getcwd()
# print("current directory is : " + dirpath)
shutil.copyfile( dirpath +"/tools/framework/root-dummies/Makefile"      , dirpath +"/Makefile" )
shutil.copyfile( dirpath +"/tools/framework/root-dummies/project.json"  , dirpath +"/project.json" )
shutil.copyfile( dirpath +"/tools/framework/root-dummies/.gitignore"    , dirpath +"/.gitignore" )


#################################################
# first git commit
#################################################

os.system("git add Makefile")
os.system("git add project.json")
os.system("git add .gitignore")
os.system('git commit -m "[base] #INIT files"')
