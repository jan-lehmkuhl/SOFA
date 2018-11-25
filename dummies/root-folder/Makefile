
#################################################################
# system settings
#################################################################

ifeq ($(OS),Windows_NT)
    del                     	=del
    rm                      	=TODO
    mkdir                   	=md

    project_root_dir        	= ${CURDIR}

else
    del                     	=rm
    rm                      	=rm -Rf
    mkdir                   	=mkdir -p

    project_root_dir        	= $(shell pwd)

endif


###############
#### TESTS ####
###############

# needs sudo apt-get install nodejs-legacy
define GetFromProjJson
	$(shell node -p "require('./project.json').$(1)")
endef

testValue     = $(shell node -p "require('./project.json').name")
testValue2    = $(call GetFromProjJson,name)

# testValue := $(shell python project.json name)


jsontest: 
	echo "test" $(testValue)
	echo "test" $(testValue2)
#	echo "PROJECT $(PROJECT) 

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

initcfx:
	make -C tools/simulation-projects/src-cfx folder


submodules:
	cd tools; git submodule add git@gitlab.com:HS-GM_OpenFOAM/openFoamSetup.git
	cd tools; git submodule add git@gitlab.com:HS-GM_OpenFOAM/OpenFoamScripts.git
