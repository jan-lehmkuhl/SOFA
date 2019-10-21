# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_mesh.mk


# include ../../../tools/framework/global-make.mk
cadFolder       = $(shell node -p "require('./mesh.json').buildSettings.cadLink")



# standard targets 
# =============================================================================

# default mesh creating target
all: mesh view

mesh: 
	if [ -f "Allmesh" ] ; then                               \
		make -C $(cadFolder) cad                           ; \
		make updateCadLink                                   ; \
		./Allmesh                                          ; \
	else                                                     \
		make frameworkmeshing                              ; \
	fi ;



# handle framework related mesh folder
# =============================================================================

# clone case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clone


# erase all files except necessary framework related files
clear:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clear


# remove all from commited sources created files and links
clean: cleanfreecadmesh cleanframeworkmesh
	# rm -f  cad[0-9][0-9][0-9]
	rm -rf constant/polyMesh/*
	rm -rf constant/triSurface
	find . -empty -type d -delete


cleanframeworkmesh: 
	rm -f  .fileStates.data
	rm -f  [0-9]/polyMesh/*
	rm -rf constant/extendedFeatureEdgeMesh/*
	rm -rf log/*


# commit all changes inside case
commit:
	python3 ../../../tools/framework/openFoam/python/openFoam.py commit


# update report according to .json
updateReport:
	python3 ../../../tools/framework/openFoam/python/openFoam.py updateReport



# FreeCAD meshing
# =============================================================================

# linking freecad-stl to std folder for using full-control meshing
updateCadLink:
	if [ -d $(cadFolder); then   rm $(cadFolder)   ; fi ;
	ln -s   ../../cad/$(cadFolder)  $(cadFolder)
	make -C ../../cad/$(cadFolder)  linkfreecadstl
	if [ ! -d constant/triSurface ] ; then   mkdir -p constant/triSurface   ; fi ; 
	cd constant/triSurface                                                         ; \
	ln -sf ../../../../cad/$(cadFolder)/meshCase/constant/triSurface/*.stl .   ; \


# can be used to overwrite the dummy settings from full-controll meshing
copyfreecadmeshfiles: linkfreecad
	cp -rf ../../cad/$(cadFolder)/meshCase/* .


openfreecad:
	make -C ../../cad/$(cadFolder)  openfreecadgui
# and write mesh case in gui


runfreecadmesh:
	./Allmesh


cleanfreecadmesh:
	rm -f log.* 
	rm -f mesh_outside.stl
	# rm -rf gmsh


# full-control framework OpenFOAM meshing
# =============================================================================

# initialize case according to mesh.json
initOpenFoamMesh:
	python3 ../../../tools/framework/openFoam/python/openFoam.py initCase


# renew the symlinks to cad 
updateSymlinks:
	python3 ../../../tools/framework/openFoam/python/openFoam.py symlinks


# generate mesh according to mesh.json
frameworkmeshing:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py mesh


# erase last boundary layer and redo 
redoMeshLayer:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py meshLayer


# copy last timestep to constant and erase the rest
finalizeMesh:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py finalizeMesh


# erase all meshing results
cleanMesh:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py cleanMesh



# GUI operations
# =============================================================================

# open paraview
view:
	if [ ! -f "Allmesh" ] ; then                                                \
		echo "*** start foamMesh.py"                                          ; \
		python3 ../../../tools/framework/openFoam/python/foamMesh.py view     ; \
	elif [ -f "pv.foam" ] ; then                                                \
		echo "*** start paraview pv.foam"                                     ; \
		paraview pv.foam                                                      ; \
	fi ;
