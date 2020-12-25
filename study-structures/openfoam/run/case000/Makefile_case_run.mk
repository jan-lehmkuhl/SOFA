# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_case_run.mk


# include ../../../tools/framework/global-make.mk

jsonFile         = $(shell find . -name 'sofa.run*.json')
linkedMeshCase   = $(shell node -p "require('$(jsonFile)').buildSettings.meshLink")

jsonFileMeshCase = $(shell find ../../mesh/$(linkedMeshCase) -name 'sofa.mesh*.json')
linkedCadCase    = $(shell node -p "require('$(jsonFileMeshCase)').buildSettings.cadLink")



# standard targets 
# =============================================================================

# default run target
run: updateUpstreamLinks
	if [ -f "Allrun" ] ; then     \
		./Allrun                ; \
		make updateCaseReport                              ; \
	else                          \
		make frameworkrun       ; \
		make -C .. updateOverviewReport                    ; \
	fi ;


mesh: 
	make -C $(linkedMeshCase) mesh


# opens reports & paraview
view:
	make -C .. showOverviewReport
	make       showCaseReport
	make       openParaview


# remove all calculated files
clean: cleanRun cleanFreecad updateUpstreamLinks
	rm -rf doc/meshReport
	find . -empty -type d -delete
	make -C ../../../tools/framework  clean



# handle framework related run folder
# =============================================================================

# initialize case according to run.json
init:
	python3 ../../../tools/framework/scripts/sofa-tasks.py initCase


# renew the upstreamLinks to mesh
updateUpstreamLinks:
	python3 ../../../tools/framework/scripts/sofa-tasks.py upstreamLinks


# clone this case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/scripts/sofa-tasks.py clone


# erase all files except necessary framework related files
clear:
	python3 ../../../tools/framework/scripts/sofa-tasks.py clear


# commit all changes inside case
commit:
	python3 ../../../tools/framework/scripts/sofa-tasks.py commit


# update report according to .json
updateCaseReport:
	python3 ../../../tools/framework/scripts/sofa-tasks.py updateReport
	make -C .. updateOverviewReport


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
copyfreecadcasefiles: updateUpstreamLinks
	cp -rf ../../cad/$(linkedCadCase)/case/* .
	sed -i 's\MESHDIR="../meshCase"\MESHDIR="./$(linkedMeshCase)"\' Allrun


cleanFreecad: 
	rm -f constant/polyMesh


openParaview:
	if [ ! -f "Allrun" ] ; then                                                 \
		echo "*** start foamMesh.py"                                          ; \
		python3 ../../../tools/framework/openFoam/python/foamRun.py view      ; \
	else                                                                        \
		echo "*** start paraFoam -builtin"                                    ; \
		paraFoam -builtin                                                     ; \
	fi ;
