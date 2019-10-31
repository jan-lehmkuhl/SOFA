
# preparation
# =============================================================================

include ../../global-make.mk


# targets
# =============================================================================

copyLaunchJsonToProject:
	cp -f  launch.json   ../../../../.vscode
	cd ../../../../.vscode ;   git add -f launch.json


linkLaunchJsonInProject:
	cd ../../../../.vscode ; ln -s  ../tools/framework/debug/vscode/launch.json  .
