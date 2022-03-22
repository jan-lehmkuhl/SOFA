
# makefile to test openfoam


SHELL := '/bin/bash'
include ../../makefile.global.mk

.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))



#   Main
# ==========================================================

tests: clean framework-chain
	@echo "finished tests for openfoam"


framework-chain: cad001 mesh001 mesh002 mesh-overview
	@echo "finished tests for framework-chain"



#   Single Tests
# ==========================================================

cad001:
	make -C cad/cad001  stl     >               logs/cad001.log
	${remove_full_path_with_sed}                logs/cad001.log
	@python3 ../../src/testing/isGitClean.py    logs/cad001.log
	@cd cad ; ${list_content}              > ../logs/cad001.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/cad001.files.txt


mesh001: 
	make -C mesh/mesh001  mesh   >              logs/mesh001-framework.log
	@${remove_full_path_with_sed}               logs/mesh001-framework.log
	@python3 ../../src/testing/isGitClean.py    logs/mesh001-framework.log
	@cd mesh/mesh001 ;  ${list_content} > ../../logs/mesh001-framework.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/mesh001-framework.files.txt

mesh002: 
	make -C mesh/mesh002  mesh   >              logs/mesh002-freecad.log
	@${remove_full_path_with_sed}               logs/mesh002-freecad.log
	@python3 ../../src/testing/isGitClean.py    logs/mesh002-freecad.log
	@cd mesh/mesh002 ;  ${list_content} > ../../logs/mesh002-freecad.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/mesh002-freecad.files.txt


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
