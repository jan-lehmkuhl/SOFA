
# simulation-projects root-makefile in ./tools/sofa-framework

include global-make.mk
include root-dummies/makefile



# General user settings
# ===================================================================

# project-folder      	= new-project-folder



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
	sudo scripts/install-deb-packages.sh
	sudo scripts/install-r-packages.sh



# project-setup
# ===================================================================

.PHONY: clean
# PHONY says make to execute even when the depending targets haven't been updated

clean: badMagicNumberClean
	# echo; pwd; ls -la

# delete python cache files 
#    they can disturb execution
badMagicNumberClean:
	find . -wholename '*/src/fileHandling.pyc' -delete
	find . -wholename '*/__pycache__/*.cpython-*.pyc' -delete


# ideas
# ===================================================================
