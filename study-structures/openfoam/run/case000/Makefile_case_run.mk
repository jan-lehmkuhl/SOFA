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
	make -C $(linkedMeshCase)
	make run 


# default run target
run: updateUpstreamLinks
	if [ -f "Allrun" ] ; then     \
		./Allrun                ; \
		make caseReport                                    ; \
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
clean: cleanRun cleanFreecad updateUpstreamLinks
	rm -rf doc/meshReport
	find . -empty -type d -delete
	make -C ../../../tools/framework  clean



# handle framework related run folder
# =============================================================================

# initialize case according to run.json
init-case: updateUpstreamLinks
	python3 ../../../tools/framework/scripts/sofa-tasks.py initCase


# renew the upstreamLinks to mesh
updateUpstreamLinks:
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

# can be used to overwrite the dummy settings
fetch-freecad-case-setup: 
	mv  ../../cad/$(linkedCadCase)/case/0  ../../cad/$(linkedCadCase)/case/0.org
	rm  -r 0.org
	rm  -r constant
	rm  -r system
	mv  ../../cad/$(linkedCadCase)/case/* .
	sed -i 's\MESHDIR="../meshCase"\MESHDIR="./$(linkedMeshCase)"\' Allrun
	make  -C  ../../cad/$(linkedCadCase)  prune-empty-freecad-export-folders


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
