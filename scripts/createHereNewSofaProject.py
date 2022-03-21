#!/usr/bin/env python3

import os
import shutil


# init repository
# =================================================================================================

if not os.path.exists(".git"):
    os.system("git init")
if not os.path.exists("tools/sofa-framework"):
    os.system("git submodule add git@gitlab.com:sofa-framework/core.git tools/sofa-framework ")



# copy first files
# =================================================================================================
dirpath = os.getcwd()
# print("current directory is : " + dirpath)


# copy dummy files
# -----------------------------------------------------------------------------
shutil.copyfile( dirpath +"/tools/sofa-framework/root-dummies/makefile"      , dirpath +"/makefile" )
shutil.copyfile( dirpath +"/tools/sofa-framework/root-dummies/sofa.project.json"  , dirpath +"/sofa.project.json" )
shutil.copyfile( dirpath +"/tools/sofa-framework/root-dummies/.gitignore"    , dirpath +"/.gitignore" )
shutil.copyfile( dirpath +"/tools/sofa-framework/root-dummies/.gitattributes", dirpath +"/.gitattributes" )
os.system("git add makefile")
os.system("git add sofa.project.json")
os.system("git add .gitignore")
os.system("git add .gitattributes")


# alter ./.git/config
# -----------------------------------------------------------------------------
if os.path.exists("./.git/config"):
    configfile=open("./.git/config", "a+")
    appendfile=open("./tools/sofa-framework/root-dummies/gitconfig-addition", "r")
    appendstring=appendfile.read()
    configfile.write("\n"+appendstring)
else: 
    pass # we are in a repository used as submodule


# docs
# -----------------------------------------------------------------------------
if not os.path.exists("./docs"):
    os.system("make initdocs")
    os.system("git add README.md")
    os.system("git add docs/makefile")



# first git commit
# =================================================================================================

os.system('git commit -m "[sofa-framework] INIT basic files and submodules"')
