# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_mesh.mk


# include ../../../tools/framework/global-make.mk
freecadFolder       = $(shell node -p "require('./mesh.json').buildSettings.freecadLink")


# handle framework related mesh folder
# =============================================================================

# clone case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clone


# erase all files except necessary framework related files
clear:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clear


# remove all from commited sources created files and links
clean: cleanfreecadmesh
	rm -rf constant/polyMesh/points*
	rm -rf constant/polyMesh/faces*
	rm -rf constant/polyMesh/owner*
	rm -rf constant/polyMesh/neighbour*
	rm -rf constant/polyMesh/boundary*
	rm -rf constant/polyMesh/sets
	rm -rf constant/polyMesh/*
	rm -rf constant/extendedFeatureEdgeMesh/*
# Zones and levels
#*Level*
#*Zone*
	rm -rf constant/polyMesh/refinementHistory*
	rm -rf constant/polyMesh/surfaceIndex*
	rm -rf constant/triSurface
	find . -empty -type d -delete


# commit all changes inside case
commit:
	python3 ../../../tools/framework/openFoam/python/openFoam.py commit


# update report according to .json
updateReport:
	python3 ../../../tools/framework/openFoam/python/openFoam.py updateReport



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


cleanfreecadmesh:
	rm -f log.* 
	rm -f mesh_outside.stl
	# rm -rf gmsh


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
		echo "*** start foamMesh.py"                                          ; \
		python3 ../../../tools/framework/openFoam/python/foamMesh.py view     ; \
	elif [ -f "pv.foam" ] ; then                                                \
		echo "*** start paraview pv.foam"                                     ; \
		paraview pv.foam                                                      ; \
	fi ;
