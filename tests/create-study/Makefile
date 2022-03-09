
#   Main
# ==========================================================

.PHONY: tests
tests: primary-init re-init


primary-init: clean
	make run-framework
	mv terminal-output-tmp.log terminal-output-init.log


.PHONY: clean
clean: 
	rm -rf dummy



#   Helper-Targets
# ==========================================================

re-init: 
	make run-framework
	mv terminal-output-tmp.log terminal-output-reinit.log


run-framework:
	rm -f .gitignore
	python3 ../tools/framework/scripts/sofa-tasks.py   \
			initStudy   \
			--verbose   \
			--no-absolute-path   \
			--studyName  create-study/dummy   \
			--studyStructFolder tools/framework/study-structures/openfoam   \
		| tee   terminal-output-tmp.log
	git reset
	git checkout .gitignore
