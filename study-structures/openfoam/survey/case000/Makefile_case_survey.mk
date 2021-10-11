# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_case_survey.mk


ifneq ("$(wildcard ./special-targets.mk)","")
    include special-targets.mk
endif



init:
	python3 ../../../tools/framework/scripts/sofa-tasks.py initCase

upstream-links:
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

