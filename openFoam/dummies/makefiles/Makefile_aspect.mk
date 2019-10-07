# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_aspect.mk


# create a new case with the next available running number
newCase:
	python3 ../../tools/framework/openFoam/python/openFoam.py newCase


# create an overview report
overview:
	python3 ../../tools/framework/openFoam/python/openFoam.py overview


# update reports to newest version and potentially run report generation
updateReports:
	python3 ../../tools/framework/openFoam/python/openFoam.py updateReports


# update json files to newest version
updateJson:
	python3 ../../tools/framework/openFoam/python/openFoam.py updateJson


# test value
test:
	python3 ../../tools/framework/openFoam/python/openFoam.py test
