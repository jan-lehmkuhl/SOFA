# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_aspect.mk

# create a new case with the next available running number
newCase:
	python3 ../../tools/framework/openFoam/python/openFoam.py newCase

# create an overview report
overview:
	python3 ../../tools/framework/openFoam/python/openFoam.py overview

# create an overview report
updateReports:
	python3 ../../tools/framework/openFoam/python/openFoam.py updateReports

# test value
test:
	python3 ../../tools/framework/openFoam/python/openFoam.py test
