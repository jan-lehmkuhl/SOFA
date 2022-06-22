# makefile copied from ./tools/sofa-framework/study-structures/openfoam/cad/case000/makefile_case_cad.mk


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

jsonfile        = $(shell find . -name 'sofa.cad*.json')
pythonPreScript  = $(shell node -p "require('$(jsonFile)').buildSettings.pythonPreExec")
pythonPostScript = $(shell node -p "require('$(jsonFile)').buildSettings.pythonPostExec")
paraviewState   = $(shell node -p "require('$(jsonfile)').buildSettings.paraviewState")
paraviewMacro   = $(shell node -p "require('$(jsonFile)').buildSettings.paraviewMacro")


include ${FRAMEWORK_PATH}/makefile.global.mk
ifneq ("$(wildcard ./special-targets.mk)","")
    include special-targets.mk
endif


#   standard targets 
# =============================================================================

.PHONY: stl
stl: 
	@echo "no automatic stl creation provided"


freecad:
	@echo; echo "*** execute >WRITE MESH< inside freecad to provide stl files in >meshCase< ***" ;echo
	@read -p "press ENTER to continue ..." dummy
	make python-pre
	make freecad-gui
	make freecad-stl-push
	make python-post
	make paraview-macro


view:
	if [   -f native/geometry.FCStd ]; then   make freecad-gui              ; fi
	if [ ! -f native/geometry.FCStd ]; then   make frameworkview               ; fi
	make paraview
	make paraview-macro


clean: clean-freecad-output clean-vtk clean-paraview
	find . -empty -type d -delete
	make -C ${FRAMEWORK_PATH}  clean



#   framework handling
# =============================================================================

# clone case to a new case with the next available running number 
clone:
	python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py clone

clean-upstream-included: clean


python-pre: 
	@if [ -f "${pythonPreScript}" ] ; then   \
		python3 ${pythonPreScript}         ; \
	fi ;
python-post: 
	@if [ -f "${pythonPostScript}" ] ; then   \
		python3 ${pythonPostScript}         ; \
	fi ;



# Basic stl/surface handling
# =============================================================================

# check topology of stl files and write log file
checkSurfaces:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamCad.py checkSurfaces


# combine all stl files into a single regional stl
combineSTL:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamCad.py combineSTL


# erase all vtk files
clean-vtk:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamCad.py cleanVTK



# FreeCAD handling
# =============================================================================

freecad-gui:
	if [ ! -f native/geometry.FCStd ]; then cp ${FRAMEWORK_PATH}/openFoam/dummies/cad/geometry.FCStd  native/geometry.FCStd; fi
	freecad-daily native/geometry.FCStd


freecad-stl-push: 
	@echo "\n*** push freecad stl export to ./stl ***"

	# check for freecad stl file existence
	@if   ls meshCase/constant/triSurface/*.stl  >/dev/null 2>&1;  then  echo "";   else   \
		echo "ERROR: provide stl-files in meshCase/constant/triSurface \n"  ; \
		exit 1 ; \
	fi

	@# delete outdated stl files
	@mkdir -p stl ; 
	@if [ ! `find stl -prune -empty 2>/dev/null` ]          ; then     \
		echo "*** OVERWRITING/DELETING EXISTING stl-files in stl folder ***"      ; \
		ls -lA stl  ; \
		read -p "press ENTER to continue ..." dummy  ; \
	fi
	rm -f  stl/*.stl
	@echo ""

	# move freecad stl export to ./stl
	mv meshCase/constant/triSurface/*  stl 
	@echo "\n    list of moved stl files " 
	@ls -lA stl 
	@echo "" 
	make prune-empty-freecad-export-folders


prune-empty-freecad-export-folders:
	@if [ -d meshCase ] ; then  \
		find meshCase -type d -empty -delete  ; \
	fi
	@if [ -d case ] ; then  \
		find case -type d -empty -delete  ;\
	fi


clean-freecad-output:
	rm -rf meshCase
	rm -rf case
	# rm -f  stl/*



# PostProcessing
# =============================================================================

# open paraview
frameworkview:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamCad.py view


# opens paraview with the referenced state file
paraview: 
	@echo "*** loaded data is specified in state file and should be made relative from caseXXX ***"
	@${remove_paraview_variable_parts} $(paraviewState)
	paraview --state=$(paraviewState)


paraview-macro: 
	@mkdir --parents doc/paraview
	@if [ -f "${paraviewMacro}" ] ; then   \
		pvbatch ${paraviewMacro}         ; \
	fi ;

clean-paraview:
	rm -rf doc/paraview
