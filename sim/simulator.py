import numpy as np

def plotSetup(ax, minx, maxx, miny, maxy):
    padding = max((maxx - minx) // 3, (maxy - miny) // 3)
    ax.set(xlim=[minx - padding, maxx + padding], ylim=[miny - padding, maxy + padding])

def nexti(i, length):
    return (i + 1) % length


def pointInArray(point, arrayOfPoints):
    for pt in arrayOfPoints:
        if np.isclose(point, pt)[0] and np.isclose(point, pt)[1]:
            return True
    return False


def simulate(points, sequences, unitPerDot, degPerDot, turnDegPerDot):
    from advanced.quad import computeQuad
    from advanced.arc import computeArc
    from advanced.tank import computeTurns
    pltPoints = []
    for i in range(len(points)):
        ni = nexti(i, len(points))
        if sequences[i] == "line":
            pltPoints.extend(computeQuad(points[i], points[ni], unitPerDot))
        elif sequences[i] == "arc":
            pltPoints.extend(computeArc(points[i], points[ni], degPerDot))

    pltPoints = computeTurns(pltPoints, points, turnDegPerDot)
    return pltPoints


def computeWheelSpeed(vec1, vec2, robotWidth, robotLength):
    dx = vec2[0] - vec1[0]
    dy = vec2[1] - vec1[1]
    a = robotWidth / 2
    b = robotLength / 2
    omega = 0
    if np.isclose(dx, 0) and np.isclose(dy, 0):
        theta1 = np.arctan2(vec1[3], vec1[2])
        theta2 = np.arctan2(vec2[3], vec2[2])
        omega = theta2 - theta1
    fr = round(dy - dx + omega * (a + b), 3)
    fl = round(dy + dx - omega * (a + b), 3)
    rl = round(dy - dx - omega * (a + b), 3)
    rr = round(dy + dx + omega * (a + b), 3)
    return fl, fr, rl, rr