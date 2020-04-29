
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
ifeq ($(OS),Windows_NT)
	cp tools/framework/docs/dummies/Makefile docs
else
	ln -s ../tools/framework/docs/dummies/Makefile docs/Makefile
endif
	make -C docs init


initstudy:
	python3 tools/framework/scripts/sofa-tasks.py initStudy --verbose


initfoam: 
	if [ ! -d docs ] ;                    then make initdocs    ; fi ;
	if [ ! -d tools/openFoam-setup ];     then cd tools ; git submodule add git@gitlab.com:HS-GM_OpenFOAM/openFoamSetup.git openFoam-setup;     fi;
	if [ ! -d tools/openFoam-reporting ]; then cd tools ; git submodule add git@gitlab.com:HS-GM_OpenFOAM/r_openfoam openFoam-reporting;        fi;
	python3 tools/framework/scripts/sofa-tasks.py initFoam

delete:
	rm -rf study1
