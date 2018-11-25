
#################################################################
# system settings
#################################################################

ifeq ($(OS),Windows_NT)
    del                     	=del
    rm                      	=TODO
    mkdir                   	=md

    project_repository_dir  	= ${CURDIR}

else
    del                     	=rm
    rm                      	=rm -Rf
    mkdir                   	=mkdir -p

    project_repository_dir  	= $(shell pwd)

endif

