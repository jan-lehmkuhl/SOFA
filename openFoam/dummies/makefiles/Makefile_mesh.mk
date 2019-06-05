# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_mesh.mk

init:
	python3 ../../../tools/framework/openFoam/python/openFoam.py initCase

updateSymlinks:
	python3 ../../../tools/framework/openFoam/python/openFoam.py symlinks

clone:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clone

clear:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clear

commit:
	python3 ../../../tools/framework/openFoam/python/openFoam.py commit

mesh:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py mesh

meshLayer:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py meshLayer

finalizeMesh:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py finalizeMesh

cleanMesh:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py cleanMesh

view:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py view

