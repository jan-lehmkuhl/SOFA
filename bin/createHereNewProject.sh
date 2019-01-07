#!/bin/bash

#################################################
# init repository
#################################################

git init
git submodule add git@gitlab.com:schlupp/simulation-projects.git tools/framework

#################################################
# copy first files
#################################################

cp ./tools/framework/root-dummies/Makefile . 
cp ./tools/framework/root-dummies/.gitignore . 
cp ./tools/framework/root-dummies/project.json .


#################################################
# first git commit
#################################################

git add .gitignore
git add .root-project
git commit -m "[base] #INIT files"
