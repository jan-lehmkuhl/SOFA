
.PHONY: test
test: clean
	rm -f .gitignore
	python3 ../tools/framework/scripts/sofa-tasks.py   \
			initStudy   \
			--verbose   \
			--no-absolute-path   \
			--studyName  create-study/dummy   \
			--studyStructFolder tools/framework/study-structures/openfoam   \
		| tee   terminal-output.log
	git reset
	git checkout .gitignore


.PHONY: clean
clean: 
	rm -rf dummy
