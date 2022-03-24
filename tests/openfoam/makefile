
# makefile to test openfoam


SHELL := '/bin/bash'
include ../../makefile.global.mk

.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))



#   Main
# ==========================================================

tests: clean framework-chain freecad-chain mesh-overview
	@echo "finished tests for openfoam"


framework-chain: cad001 mesh001 run001 
	@echo "finished tests for framework-chain"


freecad-chain: mesh002 run002
	@echo "finished tests for freecad-chain"



#   Single Tests
# ==========================================================

cad001:
	make -C cad/cad001  stl     >               logs/cad001.log
	${remove_logs_variable_content}             logs/cad001.log
	@python3 ../../src/testing/isGitClean.py    logs/cad001.log
	@cd cad ; ${list_content}              > ../logs/cad001.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/cad001.files.txt


mesh001: 
	make -C mesh/mesh001  mesh   >              logs/mesh001-framework.log
	@${remove_logs_variable_content}            logs/mesh001-framework.log
	@python3 ../../src/testing/isGitClean.py    logs/mesh001-framework.log
	@cd mesh/mesh001 ;  ${list_content} > ../../logs/mesh001-framework.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/mesh001-framework.files.txt

write-mesh001-logs:
# only to help debugging sed
	git checkout                                logs/mesh001-framework.log
	@${remove_logs_variable_content}            logs/mesh001-framework.log
	git checkout                                logs/mesh001-framework.files.txt
	@cd mesh/mesh001 ;  ${list_content} > ../../logs/mesh001-framework.files.txt


run001: 
	make -C run/run001  run   >                 logs/run001-framework.log
	@${remove_logs_variable_content}            logs/run001-framework.log
	@python3 ../../src/testing/isGitClean.py    logs/run001-framework.log
	@cd run/run001 ;  ${list_content}   > ../../logs/run001-framework.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/run001-framework.files.txt


mesh002: 
	make -C mesh/mesh002  mesh   >              logs/mesh002-freecad.log
	@${remove_logs_variable_content}            logs/mesh002-freecad.log
	@python3 ../../src/testing/isGitClean.py    logs/mesh002-freecad.log
	@cd mesh/mesh002 ;  ${list_content} > ../../logs/mesh002-freecad.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/mesh002-freecad.files.txt

run002: 
	make -C run/run002  run   >                 logs/run002-freecad.log
	@${remove_logs_variable_content}            logs/run002-freecad.log
	@python3 ../../src/testing/isGitClean.py    logs/run002-freecad.log
	@cd run/run002 ;  ${list_content}   > ../../logs/run002-freecad.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/run002-freecad.files.txt


mesh-overview:
	@cd mesh/doc ;  ${list_content}     > ../../logs/mesh-overview.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/mesh-overview.files.txt



#   Common
# ==========================================================

clean: 
	rm -f logs/*
	make -C cad    clean-cases
	make -C mesh   clean-cases
	make -C run    clean-cases
	make -C survey clean-cases
