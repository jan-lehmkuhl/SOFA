# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_aspect.mk



# handle framework related run folder
# =============================================================================

# create a new case with the next available running number
newCase:
	python3 ../../tools/framework/openFoam/python/openFoam.py newCase


# creates an overview report for all cases
overviewReportUpdate:
	python3 ../../tools/framework/openFoam/python/openFoam.py overview


# update all case reports to newest version and potentially run report generation
updateAllCaseReports:
	python3 ../../tools/framework/openFoam/python/openFoam.py updateAllReports


# update json files to newest version
updateJson:
	python3 ../../tools/framework/openFoam/python/openFoam.py updateJson



# tests
# =============================================================================

# test value
test:
	python3 ../../tools/framework/openFoam/python/openFoam.py test
