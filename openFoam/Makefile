
include ../../../tools/simulation-projects/global-make.mk

# foamFolder      = $(shell node -p "require('../../../project.json').foamFolders[0]")


test-include:  
	echo "test-include-rm: " $(rm) 

openFoam-modules:
	cd ../../../tools; git submodule add git@gitlab.com:HS-GM_OpenFOAM/openFoamSetup.git
	cd ../../../tools; git submodule add git@gitlab.com:HS-GM_OpenFOAM/OpenFoamScripts.git

initfolder: 
	echo; echo "*** initialize folder: " $(foamFolder)
	echo "project" $(project_repository_dir) 
	echo "testValue4" $(testValue4)
	pwd 
# TODO include openFoam-modules when not already created
	# $(mkdir) foam-folder-1

