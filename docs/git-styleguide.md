# GIT Styleguide for OpenFOAM

## Objective

This Styleguide is intended to give some advise on how to write meaningfull commit messages. If commit messages are written well it gets exponentionally easier to find changes and to retrace what has been done in the project, which in turn saves money and time.

The general structure of this styleguide is a modification of the best practice guide for git commit messages published on [Jaxenter](https://jaxenter.de/leitfaden-commit-messages-scm-73887).

## Guide

The field for commit messages is split into three seperate sections. These are an **identifier** followed by a **label** which is followed by a **comment**. These elements are seperated by identifying characters as follows:

```
[Identifier] #Label 'Comment' 
```

For the first two elements there is a number of predefined keywords which have shown to cover most applications. Since this guide is under constant revision, is is possible, that some keywords might be added in the future, so it makes sense to check this guide eyery once in a while.

| [Identifier]   | #Labels    | 'Comment'                      |
| -------------- | ---------- | ------------------------------ |
| [MESH-000]     | #INIT      | 'Short description of changes' |
| [BC-000]       | #IMPLEMENT |
| [SOLVER-000]   | #CHANGE    |
| [SCHEMES-000]  | #EXTEND    |
| [SOLUTION-000] | #BUGFIX    |
| [CONTROL-000]  | #REVIEW    |
| [POST-000]     | #RELEASE   |
| [FLUID-000]    | #REVERT    |
|                | #BRANCH    |
|                | #MERGE     |
|                | #CLOSE     |

Following are some examples for better understanding:

```
[Mesh-001] #CHANGE 'cellcount+ in blockMesh'
[SOLUTION-005] #CHANGE 'PCG for p'
[BC-052] #IMPLEMENT 'porous media'
[FLUID-023] #CHANGE 'viscosity'
```

If one wants to write an extended comment for Git, this can be done by leaving the second line empty. Git will only show the first line as a short heading.

```
[BC-052] #IMPLEMENT 'porous media'

Added the porous media zone perforatedPlate to account for the pressure drop and directional changes caused by the perforated plate in the system. 
```