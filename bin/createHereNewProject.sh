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

cp ./tools/simulation-projects/dummies/root-folder/Makefile . 
cp ./tools/simulation-projects/dummies/root-folder/.gitignore . 
