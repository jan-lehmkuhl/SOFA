from paraview.simple import *

import os
import sys

sys.path.append("../../../tools/sofa-framework")
from src.jsonHandling import loadJson
from src.case import findSofaJson



def main():
    caseJson = loadJson( findSofaJson(".", "") )
    paraviewState = caseJson['caseExecutions']['paraviewState']
    if not os.path.exists(paraviewState):
        return False



    print("load pv.foam and paraview state")
    # ==========================================================

    pvfoam = OpenFOAMReader(FileName='pv.foam')
    LoadState(paraviewState, 
        DataDirectory='../shared/postStates',
        pvfoamFileName='pv.foam')

    animationScene1 = GetAnimationScene()
    timeKeeper1 = GetTimeKeeper()
    animationScene1.GoToLast()



    print("execute picture export")
    # ==========================================================

    #   export renderViews
    # ------------------------------------------------
    idx = 1
    while True:
        try:
            renderView1 = FindView('RenderView' +str(idx))

            renderView1.ViewSize = [1359, 799]
            SetActiveView(renderView1)

            print("save renderView: " +str(idx))
            os.makedirs("doc/paraview", exist_ok=True)
            SaveScreenshot('doc/paraview/renderView' +str(idx) +'.png', renderView1, ImageResolution=[1359, 798])

            idx += 1
        except:
            break


if __name__ == "__main__":
    main()
