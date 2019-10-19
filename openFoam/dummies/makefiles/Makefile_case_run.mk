# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_run.mk


# include ../../../tools/framework/global-make.mk

meshFolder       = $(shell node -p "require('./run.json').buildSettings.meshLink")
freecadFolder    = $(shell node -p "require('../../mesh/$(meshFolder)/mesh.json').buildSettings.freecadLink")


# handle framework related run folder
# =============================================================================

# initialize case according to run.json
init:
	python3 ../../../tools/framework/openFoam/python/openFoam.py initCase

# renew the symlinks to mesh
updateSymlinks:
	python3 ../../../tools/framework/openFoam/python/openFoam.py symlinks

# clone case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clone

# erase all files except necessary
clear:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clear

# commit all changes inside case
commit:
	python3 ../../../tools/framework/openFoam/python/openFoam.py commit

# update report according to .json
updateReport:
	python3 ../../../tools/framework/openFoam/python/openFoam.py updateReport


# run
# =============================================================================

# run case according to run.json
run:
	python3 ../../../tools/framework/openFoam/python/foamRun.py run

# erase all results
cleanRun:
	python3 ../../../tools/framework/openFoam/python/foamRun.py cleanRun

# open paraview
view:
	if [ ! -f "Allrun" ] ; then                                                 \
		echo "*** start foamMesh.py" ;                                          \
		python3 ../../../tools/framework/openFoam/python/foamRun.py view ;      \
	elif [ -f "pv.foam" ] ; then                                                \
		echo "*** start paraFoam -builtin" ;                                     \
		paraFoam -builtin ;                                                      \
	fi ;



# FreeCAD settings
# =============================================================================

linkfreecad:
	if [ -d cad ] ; then   rm cad   ; fi ;
	ln -s   ../../cad/$(freecadFolder)  cad
	if [ -d mesh ] ; then   rm mesh   ; fi ;
	ln -s   ../../mesh/$(meshFolder)  mesh


# can be used to overwrite the dummy settings
copyfreecadcasefiles: linkfreecad
	cp -rf ../../cad/$(freecadFolder)/case/* .
	sed -i 's\MESHDIR="../meshCase"\MESHDIR="./mesh"\' Allrun


