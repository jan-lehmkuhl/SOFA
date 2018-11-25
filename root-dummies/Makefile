
include tools/simulation-projects/global-make.mk

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
	make -C tools/simulation-projects installrequirements

init: 
	$(mkdir) docs
	cp tools/simulation-projects/docs/dummies/Makefile docs
	make -C docs initfolders
	$(mkdir) mesh

initcfx:
	make -C tools/simulation-projects/src-cfx folder

initfoam: 
	$(mkdir) $(foamFolder)
	cp tools/simulation-projects/openFoam/dummies/Makefile $(foamFolder)
	make -C $(foamFolder) initfolder

	echo; pwd
	ls -la
	echo; cd $(foamFolder) ; pwd
	ls -la $(foamFolder)

