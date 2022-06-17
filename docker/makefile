working_dir = $(shell pwd)


#   standard targets
# ====================================================================

default: run-interactive


build: 
	@echo "update local docker image"
	docker build --tag sofa-openfoam:local .



#   Docker helper targets
# ====================================================================

run-interactive: 
	# choose what is good
	@if [ -d "../.git" ]; then \
		echo "This is a standalone git-repository" ;\
		make run-interactive-core ;\
	elif [ -f "../.git" ]; then \
		echo "This git-repository is a submodule" ;\
		make run-interactive-project ;\
	else \
		echo "ERROR no git found" ;\
	fi

run-interactive-core: build
# opens the sofa-core repository
	docker run --interactive --tty --volume ${working_dir}/..:/sofa-core --workdir /sofa-core sofa-openfoam:local

run-interactive-project: build
# opens underlying sofa-project
	docker run --interactive --tty --volume ${working_dir}/../../..:/sofa-project --workdir /sofa-project sofa-openfoam:local
