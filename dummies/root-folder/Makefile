
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


#################################################################
# General user settings
#################################################################


#################################################################
# targets
#################################################################

all: 
	pwd
	echo "print project_root_dir: " 
	echo $(project_root_dir) 

initcfx:
	make -C tools/simulation-projects/src-cfx folder


submodules:
	cd tools; git submodule add git@gitlab.com:HS-GM_OpenFOAM/openFoamSetup.git
	cd tools; git submodule add git@gitlab.com:HS-GM_OpenFOAM/OpenFoamScripts.git
