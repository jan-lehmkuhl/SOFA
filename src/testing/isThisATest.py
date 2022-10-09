import os
from folderHandling import findParentFolder


def isThisAnInternalSofaTest():
    sofa_core_path = findParentFolder(".gitlab-ci.yml", allowFail=True)
    if sofa_core_path == None:
        return False
    else:
        if os.path.join(sofa_core_path, 'tests') in os.getcwd(): 
            return True
        else:
            return False
