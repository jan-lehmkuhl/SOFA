# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_run.mk


# include ../../../tools/framework/global-make.mk

meshFolder       = $(shell node -p "require('./run.json').buildSettings.meshLink")
cadFolder        = $(shell node -p "require('../../mesh/$(meshFolder)/mesh.json').buildSettings.cadLink")



# standard targets 
# =============================================================================

# default run target
run: 
	if [ -f "Allrun" ] ; then     \
		./Allrun                ; \
	else                          \
		make frameworkrun       ; \
	fi ;

mesh: 
	make -C $(meshFolder) mesh


# handle framework related run folder
# =============================================================================

# initialize case according to run.json
init:
	python3 ../../../tools/framework/openFoam/python/openFoam.py initCase


# renew the symlinks to mesh
updateSymlinks:
	python3 ../../../tools/framework/openFoam/python/openFoam.py symlinks


# clone this case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clone


# erase all files except necessary framework related files
clear:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clear


# remove all calculated files
clean: cleanRun cleanFreecad updateSymlinks
	# rm -f  mesh[0-9][0-9][0-9]


# commit all changes inside case
commit:
	python3 ../../../tools/framework/openFoam/python/openFoam.py commit


# update report according to .json
updateReport:
	python3 ../../../tools/framework/openFoam/python/openFoam.py updateReport


# run
# =============================================================================

# run case according to run.json
frameworkrun:
	python3 ../../../tools/framework/openFoam/python/foamRun.py run


# erase all results
cleanRun:
	python3 ../../../tools/framework/openFoam/python/foamRun.py cleanRun


# open paraview
view:
	if [ ! -f "Allrun" ] ; then                                                 \
		echo "*** start foamMesh.py"                                          ; \
		python3 ../../../tools/framework/openFoam/python/foamRun.py view      ; \
	elif [ -f "pv.foam" ] ; then                                                \
		echo "*** start paraFoam -builtin"                                    ; \
		paraFoam -builtin                                                     ; \
	fi ;



# FreeCAD settings
# =============================================================================

# can be used to overwrite the dummy settings
copyfreecadcasefiles: updateSymlinks
	cp -rf ../../cad/$(cadFolder)/case/* .
	sed -i 's\MESHDIR="../meshCase"\MESHDIR="./$(meshFolder)"\' Allrun


cleanFreecad: 
	rm -f constant/polyMesh
