# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_case_survey.mk

init:
	python3 ../../../tools/framework/scripts/sofa-tasks.py initCase

updateUpstreamLinks:
	python3 ../../../tools/framework/scripts/sofa-tasks.py upstreamLinks

clone:
	python3 ../../../tools/framework/scripts/sofa-tasks.py clone

mesh:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py mesh

meshLayer:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py meshLayer

cleanMesh:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py cleanMesh

view:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py view

