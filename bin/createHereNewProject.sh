#!/bin/bash

#################################################
# init repository
#################################################

git init
mkdir -p tools
cd tools
git submodule add git@gitlab.com:schlupp/simulation-projects.git
cd ..


#################################################
# copy first files
#################################################

cp ./tools/simulation-projects/root-dummies/Makefile . 
cp ./tools/simulation-projects/root-dummies/.gitignore . 
cp ./tools/simulation-projects/root-dummies/project.json .


#################################################
# first git commit
#################################################

git add .gitignore
git add .root-project
git commit -m "[base] #INIT files"
