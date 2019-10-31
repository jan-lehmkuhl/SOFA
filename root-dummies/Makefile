
# project-root Makefile 



# preparation
# =============================================================================

include tools/framework/global-make.mk

cfxFolder       = $(shell node -p "require('./project.json').cfxFolders[0]")
foamFolder      = $(shell node -p "require('./project.json').foamFolders[0]")



# requirement targets
# =============================================================================

installrequirements: 
	make -C tools/framework installrequirements
	make -C tools/framework requirementtest



# init targets
# =============================================================================

initdocs:
	$(mkdir) docs
	cp tools/framework/docs/dummies/Makefile docs
	make -C docs init


initfoam: 
	if [ ! -d docs ] ;                    then make initdocs    ; fi ;
	if [ ! -d tools/openFoam-setup ];     then cd tools ; git submodule add git@gitlab.com:HS-GM_OpenFOAM/openFoamSetup.git openFoam-setup;     fi;
	if [ ! -d tools/openFoam-reporting ]; then cd tools ; git submodule add git@gitlab.com:HS-GM_OpenFOAM/r_openfoam openFoam-reporting;        fi;
	python3 tools/framework/openFoam/python/openFoam.py initFoam


initdakota: 
	$(mkdir) dakota
	# cp make
	# make -C dakota init
