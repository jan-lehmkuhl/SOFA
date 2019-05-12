
include tools/framework/global-make.mk

cfxFolder       = $(shell node -p "require('./project.json').cfxFolders[0]")
foamFolder      = $(shell node -p "require('./project.json').foamFolders[0]")



###############
#### TESTS ####
###############

# needs sudo apt-get install nodejs-legacy
define GetFromProjJson
	$(shell node -p "require('./project.json').$(1)")
endef

testValue     = $(shell node -p "require('./project.json').name")
testValue2    = $(call GetFromProjJson,name)
testValue3    = $(shell node -p "require('./project.json').list[0]")
testValue4    = $(project_repository_dir)

# testValue := $(shell python project.json name)


jsontest: 
	echo "test1" $(testValue)
	echo "test2" $(testValue2)
	echo "test3" $(testValue3)
	echo "global-rm" $(rm)
#	echo "PROJECT $(PROJECT) 

rmfoam:
	$(rm) $(foamFolder)
	ls -la


#################################################################
# General user settings
#################################################################


#################################################################
# targets
#################################################################

all: 
	pwd
	echo "print project_root_dir: " 
	echo $(project_PROJECTroot_dir) 

installrequirements: 
	make -C tools/framework installrequirements

init: 
	$(mkdir) docs
	cp tools/framework/docs/dummies/Makefile docs
	make -C docs initfolders
	$(mkdir) mesh

initcfx:
	make -C tools/framework/src-cfx folder

initfoam: 
	if [ ! -d tools/openFoam-setup ]; 	  then cd tools ; git submodule add git@gitlab.com:HS-GM_OpenFOAM/openFoamSetup.git openFoam-setup;     fi;
	if [ ! -d tools/openFoam-reporting ]; then cd tools ; git submodule add git@gitlab.com:HS-GM_OpenFOAM/r_openfoam openFoam-reporting;        fi;
	python3 tools/framework/openFoam/python/openFoam.py initFoam

