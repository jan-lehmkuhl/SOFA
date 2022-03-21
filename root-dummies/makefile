
# project-root makefile 



# preparation
# =============================================================================

ifneq      ("$(wildcard tools/sofa-framework/global-make.mk)","")
	include tools/sofa-framework/global-make.mk
endif

cfxFolder       = $(shell node -p "require('./sofa.project.json').cfxFolders[0]")
foamFolder      = $(shell node -p "require('./sofa.project.json').foamFolders[0]")



# requirement targets
# =============================================================================

installrequirements: 
	make -C tools/sofa-framework installrequirements
	make -C tools/sofa-framework requirementtest



# init targets
# =============================================================================

initdocs:
	$(mkdir) docs
ifeq ($(OS),Windows_NT)
	cp tools/sofa-framework/docs/dummies/makefile docs
else
	ln -s ../tools/sofa-framework/docs/dummies/makefile docs/makefile
endif
	make -C docs init


initstudy:
	python3 tools/sofa-framework/src/sofa-tasks.py initStudy --verbose


initfoam: 
	if [ ! -d docs ] ;                    then make initdocs    ; fi ;
	if [ ! -d tools/openFoam-setup ];     then cd tools ; git submodule add git@gitlab.com:HS-GM_OpenFOAM/openFoamSetup.git openFoam-setup;     fi;
	if [ ! -d tools/openFoam-reporting ]; then cd tools ; git submodule add git@gitlab.com:HS-GM_OpenFOAM/r_openfoam openFoam-reporting;        fi;
	python3 tools/sofa-framework/src/sofa-tasks.py initFoam



# help tools
# =============================================================================

# archives projects current state wit date stamp to ./ARCHIVE
archive:
	$(mkdir)    ARCHIVE
	tar -vcjf ./ARCHIVE/$(notdir $(CURDIR))-$(shell date +"%Y%m%d-%I%M%p").tar.bz2   --exclude='ARCHIVE' --exclude='*.tar.gz' --exclude='*.tar.bz2'  `ls -A -1`
	ls -la    ./ARCHIVE


delete:
	rm -rf study1
