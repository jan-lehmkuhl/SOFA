
# simulation-projects root-Makefile in ./tools/framework

include global-make.mk


#################################################################
# General user settings
#################################################################

project-folder      	= new-project-folder


#################################################################
# targets
#################################################################

init: new-project project-folders project-dummy-files git-init submodules
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

installrequirements: 
	sudo apt-get update
	sudo apt-get install nodejs
# install https://nodejs.org/en/download/ for macOS


#####################################################################
# project-setup
#####################################################################

new-project: clean
	$(mkdir) $(project-folder)
#	echo; pwd; ls -la $(project-folder)

project-folders: 
	$(mkdir) $(project-folder)/docs
	$(mkdir) $(project-folder)/mesh
	$(mkdir) $(project-folder)/tools

project-dummy-files:
	cp dummies/Makefile $(project-folder)
	cp dummies/.gitignore $(project-folder)

git-init: 
	cd $(project-folder); git init
	cd $(project-folder); git add .gitignore
	cd $(project-folder); git add *
	cd $(project-folder); git commit -m "[simulation-project] #INIT from simulation-projects-repository"

submodules:
	make -C $(project-folder) submodules


.PHONY: clean
# PHONY says make to execute even when the depending targets haven't been updated

clean: 
	$(rm) $(project-folder)  
	echo; pwd; ls -la


#################################################################
# ideas
#################################################################


