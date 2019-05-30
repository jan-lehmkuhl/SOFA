
# simulation-projects root-Makefile in ./tools/framework

include global-make.mk


#################################################################
# General user settings
#################################################################

# project-folder      	= new-project-folder


#################################################################
# targets
#################################################################

# first target will be executed with make only
#	cd $(project-folder); pwd
#	make -C $(project-folder) all
# changes directory and executes target
#	echo "all done" 


#####################################################################
# installation setup
#####################################################################

exampleJsonValue     = $(shell node -p "require('./root-dummies/project.json').foamFolders[0]")

requirementtest: 
	echo "show-json-value-afterwards:   " $(exampleJsonValue) 
	python   --version
	python3  --version
	simpleFoam -help

installrequirements: 
	sudo apt-get update
	sudo apt-get install nodejs
	sudo apt-get install r-base
# install https://nodejs.org/en/download/ for macOS


#####################################################################
# project-setup
#####################################################################

.PHONY: clean
# PHONY says make to execute even when the depending targets haven't been updated

clean: 
	echo; pwd; ls -la


#################################################################
# ideas
#################################################################


