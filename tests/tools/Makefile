
replace-submodule-softlinks-with-clones: 
	rm -f openFoam-setup
	git clone https://gitlab.com/sofa-framework/openFoam-setup-templates.git  openFoam-setup
	rm -f openFoam-reporting
	git clone https://gitlab.com/sofa-framework/ofreportr-templates.git       openFoam-reporting


restore-submodule-softlinks: 
	rm -rf openFoam-setup
	rm -rf openFoam-reporting
	git checkout .
