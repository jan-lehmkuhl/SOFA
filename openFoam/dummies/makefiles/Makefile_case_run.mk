# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_case_run.mk


# include ../../../tools/framework/global-make.mk

meshFolder       = $(shell node -p "require('./run.json').buildSettings.meshLink")
cadFolder        = $(shell node -p "require('../../mesh/$(meshFolder)/mesh.json').buildSettings.cadLink")



# standard targets 
# =============================================================================

# default run target
run: updateSymlinks
	if [ -f "Allrun" ] ; then     \
		./Allrun                ; \
	else                          \
		make frameworkrun       ; \
	fi ;


mesh: 
	make -C $(meshFolder) mesh


# opens reports & paraview
view:
	make -C .. showOverviewReport
	make       showCaseReport
	make       openParaview


# remove all calculated files
clean: cleanRun cleanFreecad updateSymlinks
	rm -rf doc/meshReport
	find . -empty -type d -delete



# handle framework related run folder
# =============================================================================

# initialize case according to run.json
init:
	python3 ../../../tools/framework/scripts/sofa-tasks.py initCase


# renew the symlinks to mesh
updateSymlinks:
	python3 ../../../tools/framework/scripts/sofa-tasks.py symlinks


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
	xdg-open doc/meshReport/runReport.html


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



# FreeCAD settings
# =============================================================================

# can be used to overwrite the dummy settings
copyfreecadcasefiles: updateSymlinks
	cp -rf ../../cad/$(cadFolder)/case/* .
	sed -i 's\MESHDIR="../meshCase"\MESHDIR="./$(meshFolder)"\' Allrun


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
