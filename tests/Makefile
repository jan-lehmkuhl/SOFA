
# local test execution
tests: pipeline-tests


gitlab-pipeline: gitlab-environment-setup
	make pipeline-tests


gitlab-environment-setup:
	git clone git@gitlab.com:sofa-framework/openFoam-setup-templates.git  openFoam-setup
	git clone git@gitlab.com:sofa-framework/ofreportr-templates.git       openFoam-reporting


pipeline-tests:
	make -C create-study
	@echo ""
	@echo "*** automatic tests completed ***"
	@echo ""
