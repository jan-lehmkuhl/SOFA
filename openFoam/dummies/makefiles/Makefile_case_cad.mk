# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_cad.mk



# standard targets 
# =============================================================================

all: cad view

# writes necessary cad files from sources
cad: 
	if [   -f native/geometry.FCStd ]; then                                      \
		echo; echo "*** execute WRITE MESH inside freecad ***" ;echo           ; \
		# make openfreecadgui                                                  ; \
		make linkfreecadstl                                                    ; \
	fi

# review cad files
view:
	if [   -f native/geometry.FCStd ]; then   make openfreecadgui              ; fi
	if [ ! -f native/geometry.FCStd ]; then   make view                        ; fi



# framework folder handling
# =============================================================================

# clone case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clone


# erase all files except necessary framework related files
clear:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clear


# remove all from commited sources created files and links
clean: cleanfreecadoutput cleanVTK
	find . -empty -type d -delete


# commit all changes inside case
commit:
	python3 ../../../tools/framework/openFoam/python/openFoam.py commit



# Basic stl/surface handling
# =============================================================================

# check topology of stl files and write log file
checkSurfaces:
	python3 ../../../tools/framework/openFoam/python/foamCad.py checkSurfaces


# combine all stl files into a single regional stl
combineSTL:
	python3 ../../../tools/framework/openFoam/python/foamCad.py combineSTL


# erase all vtk files
cleanVTK:
	python3 ../../../tools/framework/openFoam/python/foamCad.py cleanVTK



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
	if [ ! -d stl ]                            ; then   mkdir stl   ; fi ;
	if [   -f stl/* ]                          ; then   rm stl/*  ; fi ; 
	if [   -d "meshCase/constant/triSurface" ] ; then   cd stl;  ln -s ../meshCase/constant/triSurface/*.stl .   ; fi ;


cleanfreecadoutput:
	rm -rf meshCase
	rm -rf case
	rm -f  stl/*



# Paraview
# =============================================================================

# open paraview
frameworkview:
	python3 ../../../tools/framework/openFoam/python/foamCad.py view

