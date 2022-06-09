
# simulation-projects root-makefile in ./tools/sofa-framework

include makefile.global.mk
include root-dummies/makefile



# general
# ===================================================================

.PHONY: docker-interactive
docker-interactive:
	make -C docker run-interactive



# framework installation and setup
# ===================================================================

exampleJsonValue     = $(shell node -p "require('./root-dummies/sofa.project.json').foamFolders[0]")

requirementtest: 
	@echo "show-json-value-afterwards:   " $(exampleJsonValue) 
	@python     --version
	@python3    --version
	@simpleFoam -help      | grep Using
	@R          --version  | grep "R version"

installrequirements: 
	sudo docker/install-deb-packages.sh
	sudo docker/install-r-packages.sh


tests-local: 
	make -C tests



# project-setup
# ===================================================================

.PHONY: clean
# PHONY says make to execute even when the depending targets haven't been updated

clean: badMagicNumberClean

# delete python cache files 
#    they can disturb execution
badMagicNumberClean:
	@find . -wholename '*/src/fileHandling.pyc' -delete
	@find . -wholename '*/__pycache__/*.cpython-*.pyc' -delete


# ideas
# ===================================================================
