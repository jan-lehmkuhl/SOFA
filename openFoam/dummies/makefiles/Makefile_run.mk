# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_run.mk

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

run:
	python3 ../../../tools/framework/openFoam/python/foamRun.py run

cleanRun:
	python3 ../../../tools/framework/openFoam/python/foamRun.py cleanRun

view:
	python3 ../../../tools/framework/openFoam/python/foamRun.py view

