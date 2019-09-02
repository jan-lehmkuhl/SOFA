
<!-- copied from tools/framework/openFoam/dummies/study-documentation.md -->

# Task List
<!-- ==================================================================================== -->
- [ ] geometry 
    - [ ] import
    - [ ] simplification
- [ ] mesh
    - [ ] first mesh
    - [ ] mesh with skewness <0,9
    - [ ] mesh study
    - [ ] mesh refinement
- [ ] setup
    - [ ] set conditions
    - [ ] define monitor points
- [ ] analysis
    - [ ] first post-analysis
    - [ ] define default-analysis
    - [ ] convergence behaviour
    - [ ] final post-analysis
- [ ] geometry optimization
- [ ] write report


<!-- #################################################################################### -->
# Short Setup Description
<!-- #################################################################################### -->

## Geometry
<!-- ==================================================================================== -->


## Physics
<!-- ==================================================================================== -->
| Domain    | Setting               | Value             | checked       |
| --------- | --------------------- | ----------------- | ------------- |
| Fluid     | Ref-Pressure          | XXX [bar]         |               |
| Fluid     | Ref-Temperature       | XXX [C]           |               |
| Fluid     | Material              | XXX               |               |
| Fluid     | Density               | XXX [kg/m^3]      |               |
| Fluid     | Buoyancy              | Non               |               |
| Inlet1    | Mass Flow / Vel       | XXX [m/s]         |               |
| Outlet1   | Pressure-BC           | 0 Pa              |               |

## File Names/Organisation
<!-- ==================================================================================== -->


<!-- #################################################################################### -->
# Simplifications
<!-- #################################################################################### -->

## Geometry/Mesh
<!-- ==================================================================================== -->
### Mesh-Log
<!-- | Mesh-Nr/Name/hash | Nodes===_ | Features      | Quality (Skewness/Yplus)  | MeshStudyNotes    |
| ----------------- | --------- | ------------- | ------------------------- | ------------------|
|                   | nodes_xxx | features_xxxx | quality_xxxxxxxxxxxxxxxx  |                   | -->

### latest mesh settings
<!-- | Mesh Group| Mesh Feature              | Setting       |
| ----------| ------------------------- | ------------- |
| Workbench-Name |                      | XXX
| general   | Mesh Type:                | ??? Tet/Prism Netz
| general   | Inflation:                | ??? mit Inflation Layer
| defaults  | Element Size              | ??? 40 mm
| sizing    | Use Adaptive Sizing       | ??? No
| sizing    | Mesh Defeat. / Size       | ??? yes / 1 mm
| sizing    | Capture Curvature         | ??? Yes
| sizing    | * Curvature Min Size      | ??? 3 mm
| sizing    | * Curvature Normal Angel  | ??? Default
| sizing    | Capture Proximity         | ??? Yes
| sizing    | * Proximity Min Size      | ??? 3 mm
| sizing    | * Num Cells Across Gap    | ??? 4
| sizing    | Proximity Size Func Source| ??? Faces and Edges
| quality   | Check Mesh Quality        | ??? Yes
| quality   | Target Skewness           | ??? 0,9
| quality   | Smoothing                 | ??? High
| inflation | Use Automatic Inflation   | ??? All Faces in Chosen Named Selection  (MR Inflation)
| inflation | Inflation Option          | ??? Last Aspect Ratio
| inflation | First Layer Height        | ??? 3 mm
| inflation | Maximum Layers            | ??? 5
| inflation | Aspect Ratio (Base/Height)| ??? 1,5
| infl. adv | Collision Avoidance       | ??? Layer Compression
| infl. adv | Fix First Layer           | ??? No
| infl. adv | Gap Factor                | ??? 0,3
| infl. adv | Maximum Heigth over Base  | ??? 1
| infl. adv | Maximum Angle             | ??? 140°
| infl. adv | Fillet Ratio              | ??? 1
| infl. adv | Use Post Smoothing (Iterations) | ??? Yes 5

MR Inflation = All Faces minus: 
* MR no-Inflation
    * XXX
* Inlet
* Outlet
* Symmetries

| Mesh result               | Value     |
| ---------------------     | --------- |
| Statistics -> Nodes       | XXX
| Quality->Max (Skewness)   | XXX
| Y+ (run044)               | XXX  -->


## Physics & Numerics
<!-- ==================================================================================== -->

<!-- | Domain    | Setting               | Value             | checked       |
| --------- | --------------------- | ----------------- | ------------- |
| Numerics  | Advection Scheme      | (High Resolution) |               |
| Numerics  | Analysis Type         | steady state      |               |
| Numerics  | SubGrid-Turbulence    | (SST) <br> (Automatic Wall Function)  ||
| Numerics  | Turbulence Numerics   | (First Order)     |               |
| Post      | Macroscopic-Turbulence|                   |               | -->


<!-- #################################################################################### -->
# Simulation Behavior
<!-- #################################################################################### -->
## Simulation-Runs Log
Def-File Name:    XXX.def

<!-- | run   | Geometry/Mesh     | Setup                         | solving           | postprocessing |
| ----- | ----------------- | ----------------------------- | ----------------- | -------------- |
| 00X   |                   |                               |                   |                | -->

## Convergence
<!-- ==================================================================================== -->
### Global Residuals & Imbalances

### Yplus & Residual Locations

### Monitor Point Stability


<!-- #################################################################################### -->
# Analysis 
<!-- #################################################################################### -->
## Analysis Type

## Numerical Confidence

## Domain Conditions

## Flow Pattern
<!-- ![](cfd-reports/XXX_001_Rep/Figure001.png)  -->


<!-- #################################################################################### -->
# preliminary construction proposals
<!-- #################################################################################### -->
