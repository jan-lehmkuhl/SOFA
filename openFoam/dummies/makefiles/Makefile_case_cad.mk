# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_cad.mk


# framework handling
# =============================================================================

# clone case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clone


# erase all files except necessary
clear:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clear


# commit all changes inside case
commit:
	python3 ../../../tools/framework/openFoam/python/openFoam.py commit


# check topology of stl files and write log file
checkSurfaces:
	python3 ../../../tools/framework/openFoam/python/foamCad.py checkSurfaces


# erase all vtk files
cleanVTK:
	python3 ../../../tools/framework/openFoam/python/foamCad.py cleanVTK


# combine all stl files into a single regional stl
combineSTL:
	python3 ../../../tools/framework/openFoam/python/foamCad.py combineSTL


# GUI handling
# =============================================================================

# opencad
openfreecad:
	if [ ! -f native/geometry.FCStd ]; then cp ../../../tools/framework/openFoam/dummies/cad/geometry.FCStd  native/geometry.FCStd; fi
	freecad native/geometry.FCStd


# readable geometry diff
difffreecad:
	git diff  --color-words  native/geometry.FCStd


# open paraview
view:
	python3 ../../../tools/framework/openFoam/python/foamCad.py view

