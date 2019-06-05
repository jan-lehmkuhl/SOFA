# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_run.mk

# initialize case according to run.json
init:
	python3 ../../../tools/framework/openFoam/python/openFoam.py initCase

# renew the symlinks to mesh
updateSymlinks:
	python3 ../../../tools/framework/openFoam/python/openFoam.py symlinks

# clone case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clone

# erase all files except necessary
clear:
	python3 ../../../tools/framework/openFoam/python/openFoam.py clear

# commit all changes inside case
commit:
	python3 ../../../tools/framework/openFoam/python/openFoam.py commit

# run case according to run.json
run:
	python3 ../../../tools/framework/openFoam/python/foamRun.py run

# erase all results
cleanRun:
	python3 ../../../tools/framework/openFoam/python/foamRun.py cleanRun

# open paraview
view:
	python3 ../../../tools/framework/openFoam/python/foamRun.py view

