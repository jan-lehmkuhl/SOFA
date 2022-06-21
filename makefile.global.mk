

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

# set localisation for fixed ls sorting
export LC_ALL=en_US.UTF-8



#   helper actions
# ===================================================================

#   Paraview
# ----------------------------------------------------------

remove_paraview_variable_parts = sed --in-place --regexp-extended --expression \
	"s/(<Element index=\"0\" value=\")(.*)(pv\.foam\"\/>)/\1\3/g"



#   testing
# ----------------------------------------------------------
list_content = ls --almost-all -g --no-group \
    --time-style='+' --human-readable --group-directories-first --classify --recursive  \
    | sed -re 's/^[^ ]* //'   \
    | sed -e 's/,/./g'  \
    | sed -re 's/([1-9] )( *[ 1-9][0-9]{0,2})(  [a-zA-Z]*)/\1tiny\3/g' \
    | sed -re 's/^([0-9]{0,3})(\.[0-9])*([KM])/xxx\3/g' \
    | sed -re 's/([1-9] )([ 1-9]\.[0-9])([KM]  .*)/\1x.x\3/g' \
    | sed -re 's/^([0-9] )?( ?[0-9]{0,3})(\.[0-9])*([KM]  )/\1xxx\4/g'

# SED notes: 
#   - remove empty double lines
#   - replace , by .
#   - replace plain digigs by tiny
#   - replace folder summary
#   - replace numbers with dots (optional)
#   - replace numbers with multiplier


remove_logs_variable_content = sed --in-place --regexp-extended --expression \
    "s/(make.*'\/)(.*)(tests.*)/\1\3/g; \
    s/(^make\[)[1-9](\]: )/\1x\2/g; \
    s/([0-9]:[0-9]{2}:[0-9]{2}.[0-9]{6})/x:xx:xx.xxxxxx/g; \
    s/([0-9]{2}:[0-9]{2}.[0-9]{2})/xx:xx:xx/g; \
	s/(on )(.*)( using)/\1LocalMachine\3/g; \
	s/(Date   : )(.*) [0-9]{2} [0-9]{4}/\1xxx xx xxxx/g; \
	s/(Host   : )\".*\"/\1\"LocalMachine\"/g; \
	s/(PID    : )[0-9]{3,7}/\1xxxxxx/g; \
	s/( = )[0-9\.]* s/\1x.xx s/g; \
	s/(Case   : )(\/.*)(\/tests.*)/\1\3/g; \
	s/(\")(\/.*)(\/tests.*\")/\1\3/g; \
	s/( )(\/.*)(\/tests.*)/\1\3/g; \
	s/(Slaves : ).*/\1xxx/g; \
	s/(.* in )([0-9][0-9\.]*) s/\1xxx s/g; \
	s/(^R version )([0-9]\..*)/\1 x.x.x \.\.\./g; \
	s/(Copyright \(C\) )([0-9]{4})/\1xxxx/g; \
	s/( --mathjax=rmdformats )/ /g; \
	s/(.*template \/)([a-z]\S*)(\.html.*)/\1XXX\.html\3/g; \
	s/(.*\/tmp)(.*)(\.html.*)/\1xxxx\3/g"
