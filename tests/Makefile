
# local test execution
tests: pipeline-tests


gitlab-pipeline: gitlab-environment-setup
	make pipeline-tests


gitlab-environment-setup:
	rm -f tools/openFoam-setup
	git clone https://gitlab.com/sofa-framework/openFoam-setup-templates.git  tools/openFoam-setup
	rm -f tools/openFoam-reporting
	git clone https://gitlab.com/sofa-framework/ofreportr-templates.git       tools/openFoam-reporting


pipeline-tests:
	make -C create-study
	@echo ""
	@echo "*** pipeline tests completed ***"
	@echo ""
