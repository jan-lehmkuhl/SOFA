
# preparation
# =============================================================================

include ../../makefile.global.mk


# targets
# =============================================================================

copyLaunchJsonToProject:
	cp -f  launch.json   ../../../../.vscode
	cd ../../../../.vscode ;   git add -f launch.json


linkLaunchJsonInProject:
	cd ../../../../.vscode ; ln -s  ../tools/sofa-framework/debug/vscode/launch.json  .
