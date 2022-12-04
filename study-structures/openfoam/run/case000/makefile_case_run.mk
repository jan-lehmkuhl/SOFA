# makefile copied from ./tools/sofa-framework/openFoam/dummies/makefiles/makefile_case_run.mk


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

jsonFile         = $(shell find . -name 'sofa.run*.json')
linkedMeshCase   = $(shell node -p "require('$(jsonFile)').sofaAspectLinks.meshLink")
pythonPreScript  = $(shell node -p "require('$(jsonFile)').caseExecutions.pythonPreExec")
pythonPostScript = $(shell node -p "require('$(jsonFile)').caseExecutions.pythonPostExec")
paraviewState    = $(shell node -p "require('$(jsonFile)').caseExecutions.paraviewState")
paraviewMacro    = $(shell node -p "require('$(jsonFile)').caseExecutions.paraviewMacro")
rReport          = $(shell node -p "require('$(jsonFile)').caseExecutions.RMarkdownReport")

jsonFileMeshCase = $(shell find ../../mesh/$(linkedMeshCase) -name 'sofa.mesh*.json')
linkedCadCase    = $(shell node -p "require('$(jsonFileMeshCase)').sofaAspectLinks.cadLink")


include ${FRAMEWORK_PATH}/makefile.global.mk
ifneq ("$(wildcard ./special-targets.mk)","")
    include special-targets.mk
endif



# standard targets 
# =============================================================================

# default creating target
all: 
	make -C ../../mesh/$(linkedMeshCase)
	make run 

rerun: clean run

run: upstream-links
	make python-pre
	@if [ -f "Allrun" ] ; then    \
		make run-allrun         ; \
	else                          \
		make frameworkrun       ; \
	fi ;
	make python-post
	make paraview-macros
	@if [ "${rReport}" != "" ] ; then     \
		make -C .. overview-report      ; \
	fi ;


mesh: 
	make -C ../../mesh/$(linkedMeshCase) mesh


# opens reports & paraview
view:
	make -C .. show-overview-report
	make       show-case-report
	make       paraview


# remove all calculated files
clean: clean-run clean-freecad clean-report clean-paraview upstream-links
	@find . -empty -type d -delete
	make -C ${FRAMEWORK_PATH}  clean

clean-upstream-included: clean
	make -C $(linkedMeshCase) clean-upstream-included


# creates a zipped file of the current run
zip:
	tar --verbose --bzip2 --dereference --create --file ARCHIVE-$(notdir $(CURDIR))-$(shell date +"%Y%m%d-%H%M%p").tar.bz2  \
	    --exclude='$(linkedMeshCase)'  --exclude='*.tar.gz' --exclude='*.tar.bz2'  `ls -A -1`



#   framework handling
# =============================================================================

# initialize case according to run.json
init-case: upstream-links
	python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py initCase


upstream-links:
	@# renew the upstreamLinks to mesh
	@if [ -f "Allrun" ] ; then                                                   \
		sed -i 's\MESHDIR=".*"\MESHDIR="../../mesh/$(linkedMeshCase)"\' Allrun         ; \
	fi
	@python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py upstreamLinks


# clone this case to a new case with the next available running number 
clone:
	python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py clone


# update report according to .json
case-report:
	python3 ${FRAMEWORK_PATH}/study-structures/openfoam/shared/report.py


show-reports:  show-overview-report show-case-report

show-case-report: 
	xdg-open doc/runReport/runReport.html

show-overview-report:
	make -C .. show-overview-report


rstudio:
	rstudio doc/runReport/runReport.Rmd


clean-report: 
	@rm -f  .Rhistory
	@rm -rf doc/meshReport
	@rm -f  doc/runReport/.Rhistory


python-pre: 
	@if [ -f "${pythonPreScript}" ] ; then   \
		python3 ${pythonPreScript}         ; \
	fi ;
python-post: 
	@if [ -f "${pythonPostScript}" ] ; then   \
		python3 ${pythonPostScript}         ; \
	fi ;



# run
# =============================================================================

# run case according to run.json
frameworkrun:
	@python3 ${FRAMEWORK_PATH}/openFoam/python/foamRun.py run


# erase all results
clean-run:
	@python3 ${FRAMEWORK_PATH}/openFoam/python/foamRun.py cleanRun
	@rm -rf logs



# FreeCAD settings
# =============================================================================

freecad-gui:
	make -C ../../mesh/$(linkedMeshCase)  freecad-gui


# can be used to overwrite the dummy settings
freecad-case-setup-fetch: 
	mv  ../../cad/$(linkedCadCase)/case/0  ../../cad/$(linkedCadCase)/case/0.org
	@rm  -rf 0.org
	@rm  -rf constant
	@rm  -rf system
	mv  ../../cad/$(linkedCadCase)/case/* .
	make upstream-links
	make  -C  ../../cad/$(linkedCadCase)  prune-empty-freecad-export-folders


copy-0org-to-0:
	@mkdir -p   0
	cp    -rf  0.org/*  0


run-allrun:
	@make copy-0org-to-0
	./Allrun
	# check for existing results
	@find . -maxdepth 4 -type f -wholename "*/uniform/time" 2>/dev/null | grep -q . || (echo "ERROR did recognize a run to process"; exit 1)
	make case-report


clean-freecad: 
	@rm -f constant/polyMesh



# PostProcessing
# =============================================================================

# opens paraview with the referenced state file
paraview: paraview-fix-state
	paraview --state=$(paraviewState)


# opens Paraview without specified state
paraview-empty-state: 
	if [ ! -f "Allrun" ] ; then                                                 \
		echo "*** start foamMesh.py"                                          ; \
		python3 ${FRAMEWORK_PATH}/openFoam/python/foamRun.py view      ; \
	elif [ -f "pv.foam" ] ; then                                                \
		echo "*** start paraview pv.foam"                                     ; \
		paraview pv.foam                                                      ; \
	else                                                                        \
		echo "*** start paraFoam -builtin"                                    ; \
		paraFoam -builtin                                                     ; \
	fi ;
	make paraview-fix-state

paraview-fix-state:
	# Remove variable parts from Paraview state file
	@${remove_paraview_variable_parts} $(paraviewState)

paraview-macros:
	python3 ../../../tools/sofa-framework/study-structures/openfoam/shared/python-postprocessing.py
	pvbatch ../../../tools/sofa-framework/study-structures/openfoam/shared/paraview-export-all.py
	@if [ -f "${paraviewMacro}" ] ; then   \
		pvbatch ${paraviewMacro}         ; \
	fi ;

clean-paraview:
	@rm -rf doc/exports
	@rm -rf doc/plain-text-exports
	@rm -rf doc/paraview
	@rm -rf postExports
