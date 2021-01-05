# Makefile copied from ./tools/framework/study-structures/openfoam/cad/case000/Makefile_case_cad.mk

jsonfile        = $(shell find . -name 'sofa.cad*.json')
paraviewFile    = $(shell node -p "require('$(jsonfile)').buildSettings.paraview")



# standard targets 
# =============================================================================

# writes necessary stl files from sources
cad: 
	@echo "no automatic stl creation"

freecad:
	if [   -f native/geometry.FCStd ]; then                                      \
		echo; echo "*** execute WRITE MESH inside freecad to provide stl files in meshCase ***" ;echo   ; \
		# make openfreecadgui                                                  ; \
	fi


# review cad files
view:
	if [   -f native/geometry.FCStd ]; then   make openfreecadgui              ; fi
	if [ ! -f native/geometry.FCStd ]; then   make frameworkview               ; fi
	make paraview


# remove all from commited sources created files and links
clean: cleanfreecadoutput cleanVTK
	find . -empty -type d -delete
	make -C ../../../tools/framework  clean



# framework folder handling
# =============================================================================

# clone case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/scripts/sofa-tasks.py clone



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
	freecad native/geometry.FCStd & 


push-freecad-stl:
	if   ls meshCase/constant/triSurface/*.stl  >/dev/null 2>&1;  then  echo "";   else   \
		echo; echo "*** PROVIDE stl-files in meshCase/constant/triSurface ***"  ; \
		exit 1 ; \
	fi
	mkdir -p stl ; 
	if [ ! `find stl -prune -empty 2>/dev/null` ]          ; then     \
		echo; echo "*** OVERWRITING/DELETING EXISTING stl-files in stl folder ***"      ; \
		ls -lA stl  ; \
		../../../tools/framework/bin/pauseForMakefiles.py                       ; \
	fi
	echo "*** move freecad stl files to stl folder" ; \
	rm -f  stl/*.stl
	mv meshCase/constant/triSurface/*  stl  ; \
	ls -lA stl  ; \
	make prune-empty-freecad-export-folders


prune-empty-freecad-export-folders:
	if [ -d meshCase ] ; then  \
		find meshCase -type d -empty -delete  ; \
	fi
	if [ -d case ] ; then  \
		find case -type d -empty -delete  ;\
	fi


cleanfreecadoutput:
	rm -rf meshCase
	rm -rf case
	rm -f  stl/*



# Paraview
# =============================================================================

# open paraview
frameworkview:
	python3 ../../../tools/framework/openFoam/python/foamCad.py view


# opens paraview with the referenced state file
paraview: 
	@echo "*** loaded data is specified in state file and should be made relative from caseXXX ***"
	paraview --state=$(paraviewFile)  

