#!/usr/bin/env python3

import os
import shutil


# init repository
# =================================================================================================

os.system("git init")
os.system("git submodule add git@gitlab.com:schlupp/simulation-projects.git tools/framework ")


# copy first files
# =================================================================================================
dirpath = os.getcwd()
# print("current directory is : " + dirpath)

# copy dummy files
# -----------------------------------------------------------------------------
shutil.copyfile( dirpath +"/tools/framework/root-dummies/Makefile"      , dirpath +"/Makefile" )
shutil.copyfile( dirpath +"/tools/framework/root-dummies/project.json"  , dirpath +"/project.json" )
shutil.copyfile( dirpath +"/tools/framework/root-dummies/.gitignore"    , dirpath +"/.gitignore" )
shutil.copyfile( dirpath +"/tools/framework/root-dummies/.gitattributes", dirpath +"/.gitattributes" )

# alter ./.git/config
# -----------------------------------------------------------------------------
configfile=open("./.git/config", "a+")
appendfile=open("./tools/framework/root-dummies/gitconfig-addition", "r")
appendstring=appendfile.read()
configfile.write("\n"+appendstring)


# first git commit
# =================================================================================================

os.system("git add Makefile")
os.system("git add project.json")
os.system("git add .gitignore")
os.system("git add .gitattributes")
os.system('git commit -m "[base] #INIT files"')
