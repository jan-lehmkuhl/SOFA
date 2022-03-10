# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_case_mesh.mk


ifneq      ("$(wildcard ../../project.json)","")
    FRAMEWORK_PATH =    ../../tools/framework
else ifneq ("$(wildcard ../../../project.json)","")
    FRAMEWORK_PATH =    ../../../tools/framework
else ifneq ("$(wildcard ../../../../project.json)","")
    FRAMEWORK_PATH =    ../../../../tools/framework
else ifneq ("$(wildcard ../../../../../project.json)","")
    FRAMEWORK_PATH =    ../../../../../tools/framework
else
    FRAMEWORK_PATH = ERROR_NO_PROJECT_JSON_FOUND
endif

jsonFile        = $(shell find . -name 'sofa.mesh*.json')
linkedCadCase   = $(shell node -p "require('$(jsonFile)').buildSettings.cadLink")
paraviewFile    = $(shell node -p "require('$(jsonFile)').buildSettings.paraview")


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
	if [ -f "Allmesh" ] ; then                               \
		make mesh-allmesh                                  ; \
	else                                                     \
		make frameworkmeshing                              ; \
		make finalizeMesh                                  ; \
	fi ;
	make -C .. overview-report


meshshow: mesh
	make view


# opens reports & paraview
view:
	make -C .. show-overview-report
	make       show-case-report
	make       paraview


# remove all from commited sources created files and links
clean: clean-freecad-mesh clean-framework-mesh clean-report
	rm -rf constant/polyMesh/*
	rm -rf constant/triSurface
	find . -empty -type d -delete
	rm -f pvScriptMesh.py
	make -C ${FRAMEWORK_PATH}  clean
	make upstream-links

clean-upstream-included: clean
	make -C ../../cad/$(linkedCadCase) clean-upstream-included


# creates a zipped file of the current run
zip:
	tar --verbose --bzip2 --dereference --create --file ARCHIVE-$(notdir $(CURDIR))-$(shell date +"%Y%m%d-%H%M%p").tar.bz2  \
	    --exclude='$(linkedCadCase)'  --exclude='*.tar.gz' --exclude='*.tar.bz2'  `ls -A -1`



#   framework handling
# =============================================================================

# reinitialize case and copies files again
initCase: 
	python3 ${FRAMEWORK_PATH}/scripts/sofa-tasks.py newCase


upstream-links:
    # renew the upstreamLinks to cad 
	python3 ${FRAMEWORK_PATH}/scripts/sofa-tasks.py upstreamLinks


# clone case to a new case with the next available running number 
clone:
	python3 ${FRAMEWORK_PATH}/scripts/sofa-tasks.py clone


clean-framework-mesh: 
	rm -f  .fileStates.data
	rm -rf [0-9]/polyMesh/*
	rm -rf constant/extendedFeatureEdgeMesh/*
	rm -rf log/*


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
	rm -f log.* 
	rm -f mesh_outside.stl
	rm -f *_Geometry.fms
	# rm -rf gmsh



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
	rm -rf doc/meshReport


# opens paraview with the referenced state file
paraview: 
	@echo "*** loaded data is specified in state file and should be made relative from caseXXX ***"
	paraview --state=$(paraviewFile)  


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
