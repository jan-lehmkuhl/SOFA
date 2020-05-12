# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_case_survey.mk

init:
	python3 ../../../tools/framework/scripts/sofa-tasks.py initCase

updateSymlinks:
	python3 ../../../tools/framework/scripts/sofa-tasks.py symlinks

clone:
	python3 ../../../tools/framework/scripts/sofa-tasks.py clone

clear:
	python3 ../../../tools/framework/scripts/sofa-tasks.py clear

commit:
	python3 ../../../tools/framework/scripts/sofa-tasks.py commit

mesh:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py mesh

meshLayer:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py meshLayer

cleanMesh:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py cleanMesh

view:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py view

