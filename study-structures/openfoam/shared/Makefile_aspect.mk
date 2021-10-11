# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_aspect.mk


# standard targets 
# =============================================================================

# open overview report
show-overview-report:
	if [ $(shell basename "`pwd`" ) = "mesh" ] ; then     \
		xdg-open doc/meshOverview.html                  ; \
	elif [ $(shell basename "`pwd`" ) = "run" ] ; then     \
		xdg-open doc/runOverview.html                  ; \
	fi ;


# updates all reports in this aspect
all-reports:
	make all-case-reports
	make overview-report
	make show-overview-report


clean: 
	rm -f  .Rhistory



# handle framework related run folder
# =============================================================================

# create a new case with the next available running number
newCase:
	python3 ../../tools/framework/scripts/sofa-tasks.py newCase


# creates an overview report for all cases
    # dont updates the separate case reports
overview-report:
	python3 ../../tools/framework/scripts/sofa-tasks.py overview


# update all case reports to newest version and potentially run report generation
all-case-reports:
	python3 ../../tools/framework/scripts/sofa-tasks.py updateAllReports


rstudio:
	rstudio doc/runOverview.Rmd



# tests
# =============================================================================

# test value
test:
	python3 ../../tools/framework/scripts/sofa-tasks.py test
