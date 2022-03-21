
# docs makefile
# copied from ../tools/sofa-framework/docs/dummies/makefile 

include ../tools/sofa-framework/global-make.mk

init: folderstructure
	$(copy)  ../tools/sofa-framework/docs/dummies/main-project-readme.md   ../README.md

folderstructure: 
	for folder in             \
		3rd-party-docs        \
		discussion-notes      \
		literature            \
		reports-sources       \
		reports-compiled      \
		service-requests      \
	; do \
		$(mkdir) $$folder   ; \
		cd $$folder         ; \
		touch .gitkeep      ; \
		git add .gitkeep    ; \
		cd ..               ; \
	done
