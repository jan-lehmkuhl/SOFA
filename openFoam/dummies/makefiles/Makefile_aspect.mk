# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_aspect.mk

newCase:
	python3 ../../tools/framework/openFoam/python/openFoam.py newCase

overview:
	python3 ../../tools/framework/openFoam/python/openFoam.py overview

test:
	python3 ../../tools/framework/openFoam/python/openFoam.py test
