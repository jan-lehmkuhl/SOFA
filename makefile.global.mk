

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

list_content = ls --almost-all -g --no-group \
    --time-style='+' --human-readable --group-directories-first --classify --recursive  \
    | sed -re 's/^[^ ]* //'   \
    | sed -e 's/,/./g'  \
    | sed -re 's/([1-9] )( [ 1-9][0-9]{0,2})(  [a-zA-Z]*)/\1tiny\3/g'
remove_full_path_with_sed = sed --in-place --regexp-extended --expression \
    "s/(make.*'\/)(.*)(tests.*)/\1\3/g; \
    s/([0-9]:[0-9]{2}:[0-9]{2}.[0-9]{6})/x:xx:xx.xxxxxx/g; \
    s/([0-9]{2}:[0-9]{2}.[0-9]{2})/xx:xx:xx/g; \
	s/(on )(.*)( using)/\1LocalMachine\3/g; \
	s/(Date   : )(.*) [0-9]{2} [0-9]{4}/\1xxx xx xxxx/g; \
	s/(Host   : )\".*\"/\1\"LocalMachine\"/g; \
	s/(PID    : )[0-9]{7}/\1xxxxxx/g; \
	s/( = )[0-9\.]* s/\1x.xx s/g; \
	s/(Case   : )(\/.*)(\/sofa-framework.*)/\1\3/g; \
	s/(Slaves : ).*/\1xxx/g; \
	s/(.*\/tmp)(.*)(\.html.*)/\1xxxx\3/g"
