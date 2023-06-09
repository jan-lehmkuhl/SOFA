
# makefile to test creating a new study from scratch


SHELL := '/bin/bash'
include ../../makefile.global.mk

.PHONY: $(shell sed -n -e '/^$$/ { n ; /^[^ .\#][^ ]*:/ { s/:.*$$// ; p ; } ; }' $(MAKEFILE_LIST))



#   Main
# ==========================================================

tests: clean delete-logs primary-init re-init
	@echo "finished tests for create-study"


primary-init: clean
	make run-init
	mv logs/initStudy-tmp.log                 logs/initStudy-primary.log
	@python3 ../../src/testing/isGitClean.py  logs/initStudy-primary.log
	@cd dummy; ${list_content}           > ../logs/initStudy-primary.filelist.txt
	@python3 ../../src/testing/isGitClean.py  logs/initStudy-primary.filelist.txt
	@echo "primary-init test completed"


.PHONY: clean
clean: 
	rm -rf dummy



#   Debugging
# ==========================================================

debug: 
	touch debug-mode
	make
	@echo "DEBUG-MODE log: "
	@cat debug-mode
	@sleep 2
	@rm debug-mode



#   Helper-Targets
# ==========================================================

re-init: 
	make run-init
	mv logs/initStudy-tmp.log  logs/initStudy-reinit.log
	# cd dummy; ${listcontent} > ../content-dump-reinit.txt


run-init:
	rm -f .gitignore
	make run-single
	git reset
	git checkout .gitignore

run-single:
	python3 ../tools/sofa-framework/src/sofa-tasks.py   \
			initStudy   \
			--verbose   \
			--no-absolute-path   \
			--studyName  create-study/dummy   \
			--studyStructFolder tools/sofa-framework/study-structures/openfoam   \
		> logs/initStudy-tmp.log
	@echo "finished run-single"

delete-logs:
	rm -f  logs/initStudy-primary.log
	rm -f  logs/initStudy-primary.filelist.txt
	rm -f  logs/initStudy-reinit.log
