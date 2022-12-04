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


survey: clean upstream-links


init:
	python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py initCase

upstream-links:
	python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py upstreamLinks

clean:
	rm -rf paraview
