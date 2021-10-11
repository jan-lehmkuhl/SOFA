# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_aspect.mk

ifneq ("$(wildcard ./special-targets.mk)","")
    include special-targets.mk
endif

CASES := $(sort $(wildcard cad*/.)) $(sort $(wildcard mesh*/.)) $(sort $(wildcard run*/.))



#   framework targets
# =============================================================================

default: 

newCase:
    # create a new case with the next available running number
	python3 ../../tools/framework/scripts/sofa-tasks.py newCase


all-cases:
	$(foreach dir,$(CASES),make -C $(dir); ) 


#   clean
# --------------------------------------------------------------------
clean-aspect: 
	rm -f  .Rhistory

clean-cases: clean-aspect
	$(foreach dir,$(CASES),make -C $(dir) clean; ) 

clean-cases-upstream-included:
	$(foreach dir,$(CASES),make -C $(dir) clean-upstream-included; ) 



#   report targets 
# =============================================================================

#   show
# --------------------------------------------------------------------
show-overview-report:
	if [ $(shell basename "`pwd`" ) = "mesh" ] ; then     \
		xdg-open doc/meshOverview.html                  ; \
	elif [ $(shell basename "`pwd`" ) = "run" ] ; then    \
		xdg-open doc/runOverview.html                   ; \
	fi ;

show-all-reports: show-overview-report
	$(foreach dir,$(CASES),make -C $(dir) show-case-report; ) 


#   create
# --------------------------------------------------------------------
all-reports:
	make all-case-reports
	make overview-report
	make show-overview-report

overview-report:
	python3 ../../tools/framework/scripts/sofa-tasks.py overview

all-case-reports:
    # update all case reports to newest version and potentially run report generation
	python3 ../../tools/framework/scripts/sofa-tasks.py updateAllReports


rstudio:
	if [ $(shell basename "`pwd`" ) = "mesh" ] ; then     \
		rstudio doc/meshOverview.Rmd                    ; \
	elif [ $(shell basename "`pwd`" ) = "run" ] ; then    \
		rstudio doc/runOverview.Rmd                     ; \
	fi ;

