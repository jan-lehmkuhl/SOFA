
# simulation-projects root-Makefile in ./tools/framework

include global-make.mk



# General user settings
# ===================================================================

# project-folder      	= new-project-folder



# framework installation and setup
# ===================================================================

exampleJsonValue     = $(shell node -p "require('./root-dummies/project.json').foamFolders[0]")

requirementtest: 
	echo "show-json-value-afterwards:   " $(exampleJsonValue) 
	python   --version
	python3  --version
	simpleFoam -help

installrequirements: installrequirementsR
	sudo apt-get update
	sudo apt-get install nodejs
# install https://nodejs.org/en/download/ for macOS

installrequirementsR: 
	sudo apt-get install r-base
	sudo apt-get install pandoc
	sudo apt-get install xml2
	sudo apt-get install libssl-dev
	sudo apt-get install libxml2-dev
	sudo apt-get install libcurl4-openssl-dev



# project-setup
# ===================================================================

.PHONY: clean
# PHONY says make to execute even when the depending targets haven't been updated

clean: badMagicNumberClean
	echo; pwd; ls -la
	rm -f */__pycache__/*.cpython-36.pyc

# delete python cache files 
#    they can disturb execution
badMagicNumberClean:
	find . -name '*.pyc' -delete


# ideas
# ===================================================================

