
FSOP - Framework for Simulation and Optimization Projects
===================================================================================================

the aim of this repository is to deliver a framework to improve the opperational efficiency for simple and complex simulation projects and therefore accelerate and improve the project output.  
Actual the development is mainly for OpenFOAM and Dakota, but every scriptable Linux based simulation tool should work or can be integrated.  
To achieve this multiple measures are addressed:  

* automatic creation and usage of standard folders and files
  * improve orientation in the project for you and your colleages
  * reduce thinking and creation time for storing new files
  * reduce user errors
  * allows easy scripting
* git version control for all input (e.g. setup, documentation)
  * test old states and find faster late discovered errors
  * reduce unintentional changes
  * share or backup projects with small file sizes
* prepared standard documentation in markdown, where the related content is created
  * reduce thinking time for necessary topics and content
  * reduce documentation barrier like open an extra program and files at different places
  * allows automatic target group related documentation like short reports for your boss or long reports with all numerical information for your colleage
* seperate storage of mesh and setup files
  * allows to use the same mesh for different calculations like parameter studies
  * easy mesh replacement for multiple calculations
* use prepared OpenFoam-Setup-Files
  * reduce setup time
  * or use your own templates
* automatic comparison of similar simulation setups
  * helps to obtain the overview of different parameter runs
* scripted post processing with builtin calculation comparison and html-output
  * opening the analysis in a web browser saves time and uses less resources in the daily work
  * direct comparison of similar calculations in a parameter study allows better insights of the impact of different parameters


Get Started
===================================================================================================

Access to GitLab with ssh
---------------------------------------------------------------------------------------------------
the project downloads automatic the framework files from gitlab to `tools/framework`. Therefore you need ssh access to GitLab.  


init new project
---------------------------------------------------------------------------------------------------
to create a new project create and go to the new empty project folder and execute there `ANYPROJECT/tools/framework/bin/createHereNewProject.sh` from a previous simulation project

    mkdir <new-project-folder>
    cd <new-project-folder>
    <path-to-any-simulation-project-repository>/bin/createHereNewProject.sh

or execute the content of `./bin/createHereNewProject.py` directly after downloading from gitlab in the new project folder.  

### Push a local repository to Gitlab
If you want to share the repository on gitlab, you can create an empty project on gitlab and push the local created repository afterwards to gitlab. 

    git config --global user.name  "XXX"
    git config --global user.email "XXX@XXX.XX"

    cd EXISTING_LOCAL_REPO
    # git remote rename origin old-origin     # not necessary because there is no origin yet
    git remote add origin git@gitlab.com:NAME/GITLAB_REPO_NAME.git
    git push -u origin --all
    git push -u origin --tags


Clone an existing project repo
---------------------------------------------------------------------------------------------------
To clone an online project repo the submodules must be specified to load

    git clone --recurse-submodules git@gitlab.com:NAME/GITLAB_REPO_NAME.git
    # creates subfolder 

be aware, that the submodules are probably behind the origin/master commit


install software requirements
---------------------------------------------------------------------------------------------------
to work properly some features need special software. These should be installed after project init with:  

    cd ./tools/framework
    make installrequirements

to verifiy whether all required software works properly run: 

    cd ./tools/framework
    make requirementtest


Usage
===================================================================================================

The main idea of this framework is, that every information you need for a specific task in the simulation project is local available in the associated sub-folder and accessible by your text editor.  
Therefore the needed/main information ist stored in a documentation file, a Makefile and a json-file. In addition there are subfolders with program specific files in lower folder levels.


documentation files (*.md)
---------------------------------------------------------------------------------------------------
The documentation file should only contain the information, which is needed on a specific folder level. E.g in the root folder should only be the project specific information like who hired me to do something and which simulations will be perormed. More detailed information to the simulations will be in the documentation file in the related sub-folder


Makefiles
---------------------------------------------------------------------------------------------------
The Makefiles contain the actions you can do as Makefile-Targets. Maybe they will lead you only to deeper folders.


json-files
---------------------------------------------------------------------------------------------------
The json-file contain informations you can modify or you need to perform the calculations


folder levels
---------------------------------------------------------------------------------------------------
The project has different levels of folder-structure. 
* Project-Level
  * the root of every project and of the main git-repository
* studies
  * every project can contain multiple studies. These can be multiple CFD simulations of one specific geometry with minor changes, different meshing approaches and parameter variations.  
* aspects (cad, mesh, runs, survey)
  * every aspect contains the steps that are needed in a cfd simulation.  
* cases
  * cases are small variations of an aspect in a studie. This can be a CAD modification, a finer mesh, a setup variation or a different post survey. 

additional files
---------------------------------------------------------------------------------------------------
additional files can be added at every place, but be carefull not to distract from the main project structure.  
