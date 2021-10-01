# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_case_run.mk


# include ../../../tools/framework/global-make.mk

jsonFile         = $(shell find . -name 'sofa.run*.json')
linkedMeshCase   = $(shell node -p "require('$(jsonFile)').buildSettings.meshLink")
paraviewFile     = $(shell node -p "require('$(jsonFile)').buildSettings.paraview")

jsonFileMeshCase = $(shell find ../../mesh/$(linkedMeshCase) -name 'sofa.mesh*.json')
linkedCadCase    = $(shell node -p "require('$(jsonFileMeshCase)').buildSettings.cadLink")



# standard targets 
# =============================================================================

# default creating target
all: 
	make -C ../../mesh/$(linkedMeshCase)
	make run 


run: upstream-links
	if [ -f "Allrun" ] ; then     \
		make copy-0org-to-0     ; \
		./Allrun                ; \
		make caseReport         ; \
	else                          \
		make frameworkrun       ; \
	fi ;
	make -C .. updateOverviewReport


mesh: 
	make -C $(linkedMeshCase) mesh


# opens reports & paraview
view:
	make -C .. showOverviewReport
	make       showCaseReport
	make       paraview


# remove all calculated files
clean: cleanRun cleanFreecad upstream-links
	rm -rf doc/meshReport
	find . -empty -type d -delete
	make -C ../../../tools/framework  clean


# creates a zipped file of the current run
zip:
	tar --verbose --bzip2 --dereference --create --file ARCHIVE-$(notdir $(CURDIR))-$(shell date +"%Y%m%d-%H%M%p").tar.bz2  \
	    --exclude='$(linkedMeshCase)'  --exclude='*.tar.gz' --exclude='*.tar.bz2'  `ls -A -1`



#   framework handling
# =============================================================================

# initialize case according to run.json
init-case: upstream-links
	python3 ../../../tools/framework/scripts/sofa-tasks.py initCase


upstream-links:
    # renew the upstreamLinks to mesh
	if [ -f "Allrun" ] ; then                                                   \
		sed -i 's\MESHDIR=".*"\MESHDIR="./$(linkedMeshCase)"\' Allrun         ; \
	fi
	python3 ../../../tools/framework/scripts/sofa-tasks.py upstreamLinks


# clone this case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/scripts/sofa-tasks.py clone


# update report according to .json
caseReport:
	python3 ../../../tools/framework/study-structures/openfoam/shared/report.py


showCaseReport:
	xdg-open doc/runReport/runReport.html


showOverviewReport:
	make -C .. showOverviewReport



# run
# =============================================================================

# run case according to run.json
frameworkrun:
	python3 ../../../tools/framework/openFoam/python/foamRun.py run


# erase all results
cleanRun:
	python3 ../../../tools/framework/openFoam/python/foamRun.py cleanRun
	rm -rf logs



# FreeCAD settings
# =============================================================================

freecad-gui:
	make -C ../../mesh/$(linkedMeshCase)  freecad-gui


# can be used to overwrite the dummy settings
freecad-case-setup-fetch: 
	mv  ../../cad/$(linkedCadCase)/case/0  ../../cad/$(linkedCadCase)/case/0.org
	rm  -rf 0.org
	rm  -rf constant
	rm  -rf system
	mv  ../../cad/$(linkedCadCase)/case/* .
	sed -i 's\MESHDIR="../meshCase"\MESHDIR="./$(linkedMeshCase)"\' Allrun
	make  -C  ../../cad/$(linkedCadCase)  prune-empty-freecad-export-folders


copy-0org-to-0:
	mkdir -p   0
	cp    -rf  0.org/*  0


cleanFreecad: 
	rm -f constant/polyMesh


# opens paraview with the referenced state file
paraview: 
	@echo "*** loaded data is specified in state file and should be made relative from caseXXX ***"
	paraview --state=$(paraviewFile)  


# opens Paraview without specified state
paraview-empty-state: 
	if [ ! -f "Allrun" ] ; then                                                 \
		echo "*** start foamMesh.py"                                          ; \
		python3 ../../../tools/framework/openFoam/python/foamRun.py view      ; \
	else                                                                        \
		echo "*** start paraFoam -builtin"                                    ; \
		paraFoam -builtin                                                     ; \
	fi ;
