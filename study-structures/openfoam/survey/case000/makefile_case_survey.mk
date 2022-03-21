# makefile copied from ./tools/sofa-framework/openFoam/dummies/makefiles/makefile_case_survey.mk


ifneq      ("$(wildcard ../../sofa.project.json)","")
    FRAMEWORK_PATH =    ../../tools/sofa-framework
else ifneq ("$(wildcard ../../../sofa.project.json)","")
    FRAMEWORK_PATH =    ../../../tools/sofa-framework
else ifneq ("$(wildcard ../../../../sofa.project.json)","")
    FRAMEWORK_PATH =    ../../../../tools/sofa-framework
else ifneq ("$(wildcard ../../../../../sofa.project.json)","")
    FRAMEWORK_PATH =    ../../../../../tools/sofa-framework
else
    FRAMEWORK_PATH = ERROR_NO_PROJECT_JSON_FOUND
endif

ifneq ("$(wildcard ./special-targets.mk)","")
    include special-targets.mk
endif



init:
	python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py initCase

upstream-links:
	python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py upstreamLinks

clone:
	python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py clone

mesh:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamMesh.py mesh

meshLayer:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamMesh.py meshLayer

cleanMesh:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamMesh.py cleanMesh

view:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamMesh.py view
