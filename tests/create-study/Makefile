
listcontent = ls --almost-all -g --no-group --time-style='+' --human-readable --group-directories-first --classify --recursive   | sed -re 's/^[^ ]* //'



#   Main
# ==========================================================

.PHONY: tests
tests: primary-init re-init
	@echo "finished tests for create-study"


primary-init: clean
	make run-init
	mv terminal-output-tmp.log                  terminal-output-init.log
	@python3 ../../scripts/testing/isGitClean.py  terminal-output-init.log
	cd dummy; ${listcontent}                 > ../content-dump-init.txt
	@python3 ../../scripts/testing/isGitClean.py  content-dump-init.txt
	@echo "primary-init test completed"


.PHONY: clean
clean: 
	rm -rf dummy



#   Helper-Targets
# ==========================================================

re-init: 
	make run-init
	mv terminal-output-tmp.log terminal-output-reinit.log
	# cd dummy; ${listcontent} > ../content-dump-reinit.txt


run-init:
	rm -f .gitignore
	make run-single
	git reset
	git checkout .gitignore

run-single:
	python3 ../tools/framework/scripts/sofa-tasks.py   \
			initStudy   \
			--verbose   \
			--no-absolute-path   \
			--studyName  create-study/dummy   \
			--studyStructFolder tools/framework/study-structures/openfoam   \
		| tee  terminal-output-tmp.log
	@echo "finished run-single"
