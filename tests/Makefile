
# local test execution
tests: pipeline-tests


gitlab-pipeline: 
	make -C tools  replace-submodule-softlinks-with-clones
	make pipeline-tests


pipeline-tests:
	make -C create-study
	@echo ""
	@echo "*** pipeline tests completed ***"
	@echo ""
