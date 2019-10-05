# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_mesh.mk


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
	python3 ../../../tools/framework/openFoam/python/foamMesh.py view

