# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_cad.mk

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

checkSurfaces:
	python3 ../../../tools/framework/openFoam/python/foamCad.py checkSurfaces

cleanVTK:
	python3 ../../../tools/framework/openFoam/python/foamCad.py cleanVTK

combineSTL:
	python3 ../../../tools/framework/openFoam/python/foamCad.py combineSTL

view:
	python3 ../../../tools/framework/openFoam/python/foamCad.py view

