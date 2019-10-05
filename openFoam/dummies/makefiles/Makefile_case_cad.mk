# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_cad.mk


# framework folder handling
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


# erase all vtk files
cleanVTK:
	python3 ../../../tools/framework/openFoam/python/foamCad.py cleanVTK


# Basic stl/surface handling
# =============================================================================

# check topology of stl files and write log file
checkSurfaces:
	python3 ../../../tools/framework/openFoam/python/foamCad.py checkSurfaces


# combine all stl files into a single regional stl
combineSTL:
	python3 ../../../tools/framework/openFoam/python/foamCad.py combineSTL


# FreeCAD handling
# =============================================================================

openfreecadgui:
	if [ ! -f native/geometry.FCStd ]; then cp ../../../tools/framework/openFoam/dummies/cad/geometry.FCStd  native/geometry.FCStd; fi
	freecad native/geometry.FCStd


# readable geometry diff
difffreecad:
	git diff  --color-words  native/geometry.FCStd


# creates links in ./stl to freecad stl files for full-control OpenFOAM meshing
linkfreecadstl:
#	ln -s ../meshCase/constant/triSurface/Body001_Geometry.stl stl/Body001_Geometry.stl
	cd stl;  ln -s ../meshCase/constant/triSurface/*.stl .


clearfreecadoutput:
	rm -rf meshCase
	rm -rf case
	rm stl/*


# Paraview
# =============================================================================

# open paraview
view:
	python3 ../../../tools/framework/openFoam/python/foamCad.py view

