# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_mesh.mk


# include ../../../tools/framework/global-make.mk
freecadFolder       = $(shell node -p "require('./mesh.json').buildSettings.freecadLink")


# handle framework related mesh folder
# =============================================================================

# clone case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clone

# erase all files except framework necessary files
clear:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clear

# commit all changes inside case
commit:
	python3 ../../../tools/framework/openFoam/python/openFoam.py commit


# FreeCAD meshing
# =============================================================================

# for using full-control meshing
linkfreecad:
	if [ -d cad ] ; then   rm cad   ; fi ;
	ln -s   ../../cad/$(freecadFolder)  cad
	make -C ../../cad/$(freecadFolder)  linkfreecadstl


# can be used to overwrite the dummy settings from full-controll meshing
copyfreecadmeshfiles: linkfreecad
	cp -rf ../../cad/$(freecadFolder)/meshCase/* .


openfreecad:
	make -C ../../cad/$(freecadFolder)  openfreecadgui
# and write mesh case in gui


runfreecadmesh:
	./Allmesh


# full-control OpenFOAM meshing operations
# =============================================================================

# initialize case according to mesh.json
initOpenFoamMesh:
	python3 ../../../tools/framework/openFoam/python/openFoam.py initCase


# renew the symlinks to cad 
updateSymlinks:
	python3 ../../../tools/framework/openFoam/python/openFoam.py symlinks

# generate mesh according to mesh.json
mesh:
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
		echo "*** start foamMesh.py" ;                                          \
		python3 ../../../tools/framework/openFoam/python/foamMesh.py view ;     \
	elif [ -f "pv.foam" ] ; then                                                \
		echo "*** start paraview pv.foam" ;                                     \
		paraview pv.foam ;                                                      \
	fi ;
