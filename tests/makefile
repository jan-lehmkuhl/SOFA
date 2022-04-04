
# local test execution
tests: pipeline-tests local-tests
	@echo ""
	@echo "*** local tests completed ***"
	@echo ""


gitlab-pipeline: 
	make pipeline-tests
	@echo ""
	@echo "*** pipeline tests completed ***"
	@echo ""



#   Debugging
# ==========================================================

debug:
	make -C create-study debug
	make -C openfoam debug


pipeline-tests:
	make -C create-study


local-tests: 
	make -C openfoam


include ../root-dummies/makefile
