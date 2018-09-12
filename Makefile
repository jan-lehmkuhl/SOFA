
#################################################################
# system settings
#################################################################

# special commands 
# mkdir for windows and Linux


#################################################################
# General user settings
#################################################################



project-folder      	= new-project-folder
# special folders


#################################################################
# targets
#################################################################

all: new-project
# first target will be executed with make only
#	cd $(project-folder); pwd
	make -C $(project-folder) all
# changes directory and executes target
	echo "all done" 

new-project: clean
	mkdir $(project-folder)
	mkdir $(project-folder)/tools
	cp dummies/Makefile $(project-folder)
#	echo; pwd; ls -la
#	echo; pwd; ls -la $(project-folder)



.PHONY: clean
# PHONY says make to execute even when the depending targets haven't been updated
clean: 
	rm -rf $(project-folder)  
#	echo; pwd; ls -la


#################################################################
# ideas
#################################################################


