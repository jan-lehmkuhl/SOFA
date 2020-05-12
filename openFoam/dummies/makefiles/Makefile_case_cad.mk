# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_case_cad.mk



# standard targets 
# =============================================================================

all: cad view


# writes necessary cad files from sources
cad: 
	if [   -f native/geometry.FCStd ]; then                                      \
		echo; echo "*** execute WRITE MESH inside freecad to provide stl files in meshCase ***" ;echo   ; \
		# make openfreecadgui                                                  ; \
		make linkfreecadstl                                                    ; \
	fi


# review cad files
view:
	if [   -f native/geometry.FCStd ]; then   make openfreecadgui              ; fi
	if [ ! -f native/geometry.FCStd ]; then   make frameworkview               ; fi


# remove all from commited sources created files and links
clean: cleanfreecadoutput cleanVTK
	find . -empty -type d -delete



# framework folder handling
# =============================================================================

# clone case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/scripts/sofa-tasks.py clone


# erase all files except necessary framework related files
clear:
	python3 ../../../tools/framework/scripts/sofa-tasks.py clear


# commit all changes inside case
commit:
	python3 ../../../tools/framework/scripts/sofa-tasks.py commit



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


# creates links from freecad-exported stl-files to the cadXXX/stl folder
    # freecad stl files are exported to ./meshCase/constant/triSurface
    # cadXXX/stl/*.stl files are necessary for full-control OpenFOAM meshing
linkfreecadstl:
	if [ -f native/geometry.FCStd ] ; then     \
	if   ls meshCase/constant/triSurface/*.stl  >/dev/null 2>&1;  then  echo "";   else   \
		echo; echo "*** PROVIDE stl-files in meshCase/constant/triSurface ***"  ; \
		../../../tools/framework/bin/pauseForMakefiles.py                       ; \
	fi ; fi
	if [ ! -d stl ]                            ; then   mkdir stl   ; fi ;
	if [   -d "meshCase/constant/triSurface" ] ; then   cd stl;  ln -sf ../meshCase/constant/triSurface/*.stl .   ; fi ;


cleanfreecadoutput:
	rm -rf meshCase
	rm -rf case
	rm -f  stl/*



# Paraview
# =============================================================================

# open paraview
frameworkview:
	python3 ../../../tools/framework/openFoam/python/foamCad.py view

