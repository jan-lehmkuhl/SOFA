#!/usr/bin/env python3

import os
import shutil


# init repository
# =================================================================================================

os.system("git init")
os.system("git submodule add git@gitlab.com:sofa-framework/core.git tools/framework ")


# copy first files
# =================================================================================================
dirpath = os.getcwd()
# print("current directory is : " + dirpath)

# copy dummy files
# -----------------------------------------------------------------------------
shutil.copyfile( dirpath +"/tools/framework/root-dummies/Makefile"      , dirpath +"/Makefile" )
shutil.copyfile( dirpath +"/tools/framework/root-dummies/sofa.project.json"  , dirpath +"/sofa.project.json" )
shutil.copyfile( dirpath +"/tools/framework/root-dummies/.gitignore"    , dirpath +"/.gitignore" )
shutil.copyfile( dirpath +"/tools/framework/root-dummies/.gitattributes", dirpath +"/.gitattributes" )
os.system("git add Makefile")
os.system("git add sofa.project.json")
os.system("git add .gitignore")
os.system("git add .gitattributes")

# alter ./.git/config
# -----------------------------------------------------------------------------
configfile=open("./.git/config", "a+")
appendfile=open("./tools/framework/root-dummies/gitconfig-addition", "r")
appendstring=appendfile.read()
configfile.write("\n"+appendstring)

# docs
# -----------------------------------------------------------------------------
os.system("make initdocs")
os.system("git add README.md")
os.system("git add docs/Makefile")


# first git commit
# =================================================================================================

os.system('git commit -m "[base] #INIT files"')
