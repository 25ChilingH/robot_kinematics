from sim import main
from carPython.sim.utils import computeWheelSpeed
from carPython.sim.utils import nexti

pltPoints = main.pltPoints
currentIdx = 0


def getWheelSpeedsAndDelay():
    nextIdx = nexti(currentIdx, len(pltPoints))
    wheelSpeeds = computeWheelSpeed(
        pltPoints[currentIdx],
        pltPoints[nextIdx],
        main.delay,
        main.robotWidth,
        main.robotLength,
    )
    currentIdx = nextIdx
    return wheelSpeeds, main.delay
