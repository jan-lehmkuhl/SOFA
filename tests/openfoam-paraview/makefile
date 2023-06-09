
# makefile to test openfoam


SHELL := '/bin/bash'
include ../../makefile.global.mk

.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))



#   Main
# ==========================================================

tests: clean-and-remove-logs freecad-chain mesh-overview
	@echo "finished tests for openfoam"


freecad-chain: cad001 mesh001 run001 survey001
	@echo "finished tests for freecad-chain"



#   Debugging
# ==========================================================

debug: 
	touch debug-mode
	make tests
	@echo "DEBUG-MODE log: "
	@cat debug-mode
	@sleep 2
	@rm debug-mode

write-mesh001-logs:
# only to help debugging sed
	git checkout                                logs/mesh001-framework.log
	@${remove_logs_variable_content}            logs/mesh001-framework.log
	git checkout                                logs/mesh001-framework.files.txt
	@cd mesh/mesh001 ;  ${list_content} > ../../logs/mesh001-framework.files.txt



#   Single Tests
# ==========================================================

cad001:
	make -C cad/cad001  stl     >               logs/cad001.log
	${remove_logs_variable_content}             logs/cad001.log
	@python3 ../../src/testing/isGitClean.py    logs/cad001.log
	@cd cad ; ${list_content}              > ../logs/cad001.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/cad001.files.txt

mesh001: 
	make -C mesh/mesh001  mesh   >              logs/mesh001-freecad.log
	@${remove_logs_variable_content}            logs/mesh001-freecad.log
	@python3 ../../src/testing/isGitClean.py    logs/mesh001-freecad.log
	@cd mesh/mesh001 ;  ${list_content} > ../../logs/mesh001-freecad.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/mesh001-freecad.files.txt

run001: 
	make -C run/run001  run   >                 logs/run001-freecad.log
	@${remove_logs_variable_content}            logs/run001-freecad.log
	@python3 ../../src/testing/isGitClean.py    logs/run001-freecad.log
	@cd run/run001 ;  ${list_content}   > ../../logs/run001-freecad.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/run001-freecad.files.txt

survey001: 
	make -C survey/survey001  survey   >        logs/survey001.log
	@${remove_logs_variable_content}            logs/survey001.log
	@python3 ../../src/testing/isGitClean.py    logs/survey001.log
	@cd survey/survey001 ;  ${list_content}   > ../../logs/survey001.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/survey001.files.txt

mesh-overview:
	@cd mesh/doc ;  ${list_content}     > ../../logs/mesh-overview.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/mesh-overview.files.txt



#   Common
# ==========================================================

clean: 
	git checkout -- logs
	make -C cad    clean-cases
	make -C mesh   clean-cases
	make -C run    clean-cases
	make -C survey clean-cases

clean-and-remove-logs: clean
	rm -f logs/*
