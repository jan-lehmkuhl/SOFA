# Makefile copied from ./tools/framework/openFoam/dummies/makefiles/Makefile_case_mesh.mk


# include ../../../tools/framework/global-make.mk
jsonFile        = $(shell find . -name 'sofa.mesh*.json')
linkedCadCase   = $(shell node -p "require('$(jsonFile)').buildSettings.cadLink")
paraviewFile    = $(shell node -p "require('$(jsonFile)').buildSettings.paraview")



# standard targets 
# =============================================================================

# default mesh creating target
all: 
	make -C $(linkedCadCase) cad                           ; \
	make mesh 


# creates mesh
    # NOTE: update cad folder before
mesh: updateUpstreamLinks
	if [ -f "Allmesh" ] ; then                               \
		make linkCadStlFiles                               ; \
		./Allmesh                                          ; \
		checkMesh  | tee log.checkMesh                     ; \
		make caseReport                                    ; \
	else                                                     \
		make frameworkmeshing                              ; \
		make finalizeMesh                                  ; \
	fi ;
	make -C .. updateOverviewReport


meshshow: mesh
	make view


# opens reports & paraview
view:
	make -C .. showOverviewReport
	make       showCaseReport
	make       paraview


# remove all from commited sources created files and links
clean: cleanfreecadmesh cleanframeworkmesh cleanReport updateUpstreamLinks
	rm -rf constant/polyMesh/*
	rm -rf constant/triSurface
	find . -empty -type d -delete
	rm -f pvScriptMesh.py
	make -C ../../../tools/framework  clean



# handle framework related mesh folder
# =============================================================================

# clone case to a new case with the next available running number 
clone:
	python3 ../../../tools/framework/scripts/sofa-tasks.py clone


cleanframeworkmesh: 
	rm -f  .fileStates.data
	rm -f  [0-9]/polyMesh/*
	rm -rf constant/extendedFeatureEdgeMesh/*
	rm -rf log/*


# run case report according to .json
caseReport: updateUpstreamLinks
	python3 ../../../tools/framework/study-structures/openfoam/shared/report.py


showReports:  showOverviewReport showCaseReport

showCaseReport:
	xdg-open doc/meshReport/meshReport.html

showOverviewReport:
	make -C .. showOverviewReport



# FreeCAD meshing
# =============================================================================


# links cadXXX/stl/*.stl to constant/triSurface
    # >make -C CAD linkfreecadstl< links stl-files in meshCase to cadXXX/stl/*.stl 
linkCadStlFiles:
	if [ -f "Allmesh" ]  &&  [ "$(linkedCadCase)" != "" ]  ; then                             \
		make -C ../../cad/$(linkedCadCase)  linkfreecadstl                                  ; \
		if [ ! -d constant/triSurface ] ; then   mkdir -p constant/triSurface   ; fi    ; \
		cd constant/triSurface                                                          ; \
		ln -sf ../../../../cad/$(linkedCadCase)/stl/*.stl  .                                ; \
		echo "following files exist now in constant/triSurface" ;  ls -l                ; \
	fi ;


# imports and overwrites mesh settings from freecad export CAD/meshCase/system
    # can be used to overwrite the dummy settings from full-controll meshing
    # stl files remain in meshCase
fetchFreecadMeshSetup: linkCadStlFiles
	mv    -f  ../../cad/$(linkedCadCase)/meshCase/Allmesh   .
	mkdir -p  system
	mv    -f  ../../cad/$(linkedCadCase)/meshCase/system/*  ./system


openfreecad:
	make -C ../../cad/$(linkedCadCase)  openfreecadgui
# and write mesh case in gui


runfreecadmesh:
	./Allmesh


cleanfreecadmesh:
	rm -f log.* 
	rm -f mesh_outside.stl
	rm -f *_Geometry.fms
	# rm -rf gmsh



# full-control framework OpenFOAM meshing
# =============================================================================

# renew the upstreamLinks to cad 
updateUpstreamLinks:
	python3 ../../../tools/framework/scripts/sofa-tasks.py upstreamLinks


# generate mesh according to mesh.json
frameworkmeshing:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py mesh


# erase last boundary layer and redo 
redoMeshLayer:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py meshLayer


# copy last timestep to constant
finalizeMesh:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py finalizeMesh


# erase all meshing results
cleanMesh:
	python3 ../../../tools/framework/openFoam/python/foamMesh.py cleanMesh

cleanReport:
	rm -rf doc/meshReport


# opens paraview with the referenced state file
paraview: 
	@echo "*** loaded data is specified in state file and should be made relative from caseXXX ***"
	paraview --state=$(paraviewFile)  


# opens Paraview without specified state
paraview-empty-state: 
	if [ ! -f "Allmesh" ] ; then                                                \
		echo "*** start foamMesh.py"                                          ; \
		python3 ../../../tools/framework/openFoam/python/foamMesh.py view     ; \
	elif [ -f "pv.foam" ] ; then                                                \
		echo "*** start paraview pv.foam"                                     ; \
		paraview pv.foam                                                      ; \
	else                                                                        \
		echo "*** start paraFoam"                                             ; \
		paraFoam                                                              ; \
	fi ;
