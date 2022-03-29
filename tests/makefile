
# local test execution
tests: pipeline-tests local-tests
	@echo ""
	@echo "*** local tests completed ***"
	@echo ""


gitlab-pipeline: 
	make -C tools  replace-submodule-softlinks-with-clones
	make pipeline-tests


pipeline-tests:
	make -C create-study
	@echo ""
	@echo "*** pipeline tests completed ***"
	@echo ""


local-tests: 
	make -C openfoam


include ../root-dummies/makefile
