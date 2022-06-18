
#   Main Targets
# ==========================================================

# local test execution
tests: pipeline-tests additional-local-tests
	@echo ""
	@echo "*** local tests completed ***"
	@echo ""


gitlab-pipeline: 
	make pipeline-tests
	@echo ""
	@echo "*** pipeline tests completed ***"
	@echo ""


clean:
	make -C create-study clean
	make -C openfoam clean



#   Debugging
# ==========================================================

debug:
	make -C create-study debug
	make -C openfoam debug



#   Test Collections
# ==========================================================

#   GitLab Pipeline Tests
# ------------------------------------------------
pipeline-tests:
	make -C create-study


#   Local tests
# ------------------------------------------------
additional-local-tests:
	make -C openfoam
	@echo "local-tests succeeded"


include ../root-dummies/makefile
