# makefile copied from ./tools/sofa-framework/openFoam/dummies/makefiles/makefile_case_mesh.mk


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

jsonFile        = $(shell find . -name 'sofa.mesh*.json')
linkedCadCase   = $(shell node -p "require('$(jsonFile)').sofaAspectLinks.cadLink")
pythonPreScript = $(shell node -p "require('$(jsonFile)').caseExecutions.pythonPreExec")
pythonPostScript= $(shell node -p "require('$(jsonFile)').caseExecutions.pythonPostExec")
paraviewState   = $(shell node -p "require('$(jsonFile)').caseExecutions.paraviewState")
paraviewMacro   = $(shell node -p "require('$(jsonFile)').caseExecutions.paraviewMacro")
rReport         = $(shell node -p "require('$(jsonFile)').caseExecutions.RMarkdownReport")


include ${FRAMEWORK_PATH}/makefile.global.mk
ifneq ("$(wildcard ./special-targets.mk)","")
    include special-targets.mk
endif



# standard targets 
# =============================================================================

# default creating target
all: 
	make -C ../../cad/$(linkedCadCase)
	make mesh 


mesh: upstream-links
    # NOTE: update cad folder before
	make python-pre
	@if [ -f "Allmesh" ] ; then                               \
		make mesh-allmesh                                  ; \
	else                                                     \
		make frameworkmeshing                              ; \
		make finalizeMesh                                  ; \
	fi ;
	make python-post
	make paraview-macros
	@if [ "${rReport}" != "" ] ; then     \
		make -C .. overview-report      ; \
	fi ;


meshshow: mesh
	make view


# opens reports & paraview
view:
	make -C .. show-overview-report
	make       show-case-report
	make       paraview


# remove all from commited sources created files and links
clean: clean-freecad-mesh clean-framework-mesh clean-report clean-paraview
	@rm -rf constant/polyMesh/*
	@rm -rf constant/triSurface
	@find . -empty -type d -delete
	@rm -f pvScriptMesh.py
	make -C ${FRAMEWORK_PATH}  clean
	@make upstream-links

clean-upstream-included: clean
	@make -C ../../cad/$(linkedCadCase) clean-upstream-included


# creates a zipped file of the current run
zip:
	tar --verbose --bzip2 --dereference --create --file ARCHIVE-$(notdir $(CURDIR))-$(shell date +"%Y%m%d-%H%M%p").tar.bz2  \
	    --exclude='$(linkedCadCase)'  --exclude='*.tar.gz' --exclude='*.tar.bz2'  `ls -A -1`



#   framework handling
# =============================================================================

# reinitialize case and copies files again
init-case: upstream-links
	python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py initCase


upstream-links:
    # renew the upstreamLinks to cad 
	@python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py upstreamLinks


# clone case to a new case with the next available running number 
clone:
	python3 ${FRAMEWORK_PATH}/src/sofa-tasks.py clone


clean-framework-mesh: 
	@rm -f  .fileStates.data
	@rm -rf [0-9]/polyMesh/*
	@rm -rf constant/extendedFeatureEdgeMesh/*
	@rm -rf log/*


# run case report according to .json
case-report: upstream-links
	python3 ${FRAMEWORK_PATH}/study-structures/openfoam/shared/report.py


show-reports:  show-overview-report show-case-report

show-case-report:
	xdg-open doc/meshReport/meshReport.html

show-overview-report:
	make -C .. show-overview-report


rstudio:
	rstudio doc/meshReport/meshReport.Rmd

python-pre: 
	@if [ -f "${pythonPreScript}" ] ; then   \
		python3 ${pythonPreScript}         ; \
	fi ;
python-post: 
	@if [ -f "${pythonPostScript}" ] ; then   \
		python3 ${pythonPostScript}         ; \
	fi ;



# FreeCAD meshing
# =============================================================================

freecad-gui:
	make -C ../../cad/$(linkedCadCase)  freecad
	make freecad-mesh-setup-fetch


freecad-mesh-setup-fetch: clean
    # imports and overwrites mesh settings from freecad export CAD/meshCase/system
    # can be used to overwrite the dummy settings from full-controll meshing

	@if   ls ../../cad/$(linkedCadCase)/meshCase/constant/triSurface/*.stl  >/dev/null 2>&1;  then   \
		make  -C  ../../cad/$(linkedCadCase)  freecad-stl-push ; \
	fi

	@echo "\n*** fetch FreeCAD meshCase files ***" 
	@read -p "press ENTER to start overwriting files ..." dummy 
	mv    -f  ../../cad/$(linkedCadCase)/meshCase/Allmesh   .
	mkdir -p  system
	rm    -f  system/*
	mv    -f  ../../cad/$(linkedCadCase)/meshCase/system/*  ./system
	make  -C  ../../cad/$(linkedCadCase)  prune-empty-freecad-export-folders
	make upstream-links


mesh-allmesh: 
	./Allmesh
	@test -e constant/polyMesh/points && echo "mesh exists" || (echo "mesh not exists"; exit 1)
	checkMesh  | tee log.checkMesh
	make case-report


clean-freecad-mesh:
	@rm -f log.* 
	@rm -f mesh_outside.stl
	@rm -f *_Geometry.fms
	@# rm -rf gmsh



# full-control framework OpenFOAM meshing
# =============================================================================

# generate mesh according to mesh.json
frameworkmeshing:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamMesh.py mesh


# erase last boundary layer and redo 
redoMeshLayer:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamMesh.py meshLayer


# copy last timestep to constant
finalizeMesh:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamMesh.py finalizeMesh


# erase all meshing results
cleanMesh:
	python3 ${FRAMEWORK_PATH}/openFoam/python/foamMesh.py cleanMesh

clean-report:
	@rm -rf doc/meshReport



# PostProcessing
# =============================================================================

# opens paraview with the referenced state file
paraview: paraview-fix-state
	paraview --state=$(paraviewState)


# opens Paraview without specified state
paraview-empty-state: 
	if [ ! -f "Allmesh" ] ; then                                                \
		echo "*** start foamMesh.py"                                          ; \
		python3 ${FRAMEWORK_PATH}/openFoam/python/foamMesh.py view     ; \
	elif [ -f "pv.foam" ] ; then                                                \
		echo "*** start paraview pv.foam"                                     ; \
		paraview pv.foam                                                      ; \
	else                                                                        \
		echo "*** start paraFoam"                                             ; \
		paraFoam                                                              ; \
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
	@rm -rf doc/paraview
	@rm -rf postExports
