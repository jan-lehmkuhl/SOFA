#!/bin/bash

#################################################
# init repository
#################################################

git init
git submodule add git@gitlab.com:schlupp/simulation-projects.git tools

#################################################
# copy first files
#################################################

cp ./tools/root-dummies/Makefile . 
cp ./tools/root-dummies/.gitignore . 
cp ./tools/root-dummies/project.json .


#################################################
# first git commit
#################################################

git add .gitignore
git add .root-project
git commit -m "[base] #INIT files"
