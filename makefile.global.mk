

# system settings
# ===================================================================

ifeq ($(OS),Windows_NT)
    del                     	=del
    rm                      	=TODO
    mkdir                   	=md
    copy                    	=copy 

    project_repository_dir  	= ${CURDIR}

else
    del                     	=rm
    rm                      	=rm -Rf
    mkdir                   	=mkdir -p
    copy                    	=cp 

    project_repository_dir  	= $(shell pwd)

endif


#   testing helpers
# ===================================================================

list_content = ls --almost-all -g --no-group --time-style='+' --human-readable --group-directories-first --classify --recursive   | sed -re 's/^[^ ]* //'   | sed -e 's/,/./g'
remove_full_path_with_sed = sed --in-place --regexp-extended --expression \
    "s/(make.*'\/)(.*)(tests.*)/\1\3/g; \
    s/([0-9]:[0-9]{2}:[0-9]{2}.[0-9]{6})/x:xx:xx.xxxxxx/g; \
	s/(.*\/tmp)(.*)(\.html.*)/\1xxxx\3/g"
