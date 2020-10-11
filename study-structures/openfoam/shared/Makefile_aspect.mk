# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_aspect.mk


# standard targets 
# =============================================================================

# open overview report
showOverviewReport:
	if [ $(shell basename "`pwd`" ) = "mesh" ] ; then     \
		xdg-open doc/meshOverview.html                  ; \
	elif [ $(shell basename "`pwd`" ) = "run" ] ; then     \
		xdg-open doc/runOverview.html                  ; \
	fi ;


# updates all reports in this aspect
updateAllReports:
	make updateCaseReports
	make updateOverviewReport
	make showOverviewReport



# handle framework related run folder
# =============================================================================

# create a new case with the next available running number
newCase:
	python3 ../../tools/framework/scripts/sofa-tasks.py newCase


# creates an overview report for all cases
    # dont updates the separate case reports
updateOverviewReport:
	python3 ../../tools/framework/scripts/sofa-tasks.py overview


# update all case reports to newest version and potentially run report generation
updateCaseReports:
	python3 ../../tools/framework/scripts/sofa-tasks.py updateAllReports


# update json files to newest version
updateJson:
	python3 ../../tools/framework/scripts/sofa-tasks.py updateJson



# tests
# =============================================================================

# test value
test:
	python3 ../../tools/framework/scripts/sofa-tasks.py test
