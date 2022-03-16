
# local test execution
tests: pipeline-tests


gitlab-pipeline: gitlab-environment-setup
	make pipeline-tests


gitlab-environment-setup:
	rm -f openFoam-setup
	git clone https://gitlab.com/sofa-framework/openFoam-setup-templates.git  openFoam-setup
	rm -f openFoam-reporting
	git clone https://gitlab.com/sofa-framework/ofreportr-templates.git       openFoam-reporting


pipeline-tests:
	make -C create-study
	@echo ""
	@echo "*** pipeline tests completed ***"
	@echo ""
