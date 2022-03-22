
# makefile to test openfoam


SHELL := '/bin/bash'
include ../../global-make.mk

.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))



#   Main
# ==========================================================

tests: framework-chain
	@echo "finished tests for openfoam"


framework-chain: 
	make -C cad/cad001  stl     >               logs/cad001.log
	${remove_full_path_with_sed}                logs/cad001.log
	@python3 ../../src/testing/isGitClean.py    logs/cad001.log
	@cd cad ; ${list_content}              > ../logs/cad001.files.txt
	@python3 ../../src/testing/isGitClean.py    logs/cad001.files.txt

	@echo "finished tests for framework-chain"


clean: 
	make -C cad    clean-cases
	make -C mesh   clean-cases
	make -C run    clean-cases
	make -C survey clean-cases
