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


def computePltPoints(points, sequences, unitPerDot, degPerDot, turnDegPerDot):
    pltPoints = []
    for i in range(len(points)):
        ni = nexti(i, len(points))
        if sequences[i] == "line":
            pltPoints.extend(computeQuad(points[i], points[ni], unitPerDot))
        elif sequences[i] == "arc":
            pltPoints.extend(computeArc(points[i], points[ni], degPerDot))

    pltPoints = computeTurns(pltPoints, points, turnDegPerDot)
    return pltPoints


def computeArrow(arcs):
    angles = []
    for i in range(len(arcs)):
        nextIdx = nexti(i, len(arcs))
        point1 = tuple(arcs[i])
        point2 = tuple(arcs[nextIdx])
        angles.append(
            [point1, np.arctan2(point2[1] - point1[1], point2[0] - point1[0])]
        )
    return angles


def computeTurns(plotpoints, points, degPerTurn):
    angles = computeArrow(plotpoints)
    arcs = []
    for i in range(len(angles)):
        nextIdx = nexti(i, len(angles))
        arcs.append(
            [
                angles[i][0][0],
                angles[i][0][1],
                np.cos(angles[i][1]),
                np.sin(angles[i][1]),
            ]
        )
        if pointInArray(angles[nextIdx][0], points):
            if angles[i][1] < angles[nextIdx][1]:
                step = np.deg2rad(degPerTurn)
            else:
                step = -np.deg2rad(degPerTurn)
            for theta in np.arange(angles[i][1], angles[nextIdx][1], step):
                arcs.append(
                    [
                        angles[nextIdx][0][0],
                        angles[nextIdx][0][1],
                        np.cos(theta),
                        np.sin(theta),
                    ]
                )
    return arcs


def computeArc(point1, point2, degPerDot):
    arcs = []
    center = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)
    r = distance(point1, center)
    offset = np.arctan2(point1[1] - center[1], point1[0] - center[0])

    for alpha in np.arange(0, np.pi, np.deg2rad(degPerDot)):
        theta = alpha + offset
        x = center[0] + r * np.cos(theta)
        y = center[1] + r * np.sin(theta)
        arcs.append([x, y])
    return arcs


def computeQuad(point1, point2, unitPerDot):
    arcs = []
    angle = np.arctan2(point2[1] - point1[1], point2[0] - point1[0])
    dist = np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    x = point1[0]
    y = point1[1]
    for i in np.arange(0, dist, unitPerDot):
        arcs.append([x, y])
        x += np.cos(angle) * unitPerDot
        y += np.sin(angle) * unitPerDot
    return arcs


def computeWheelSpeed(vec1, vec2, time, robotWidth, robotLength):
    vx = (vec2[0] - vec1[0]) / time
    vy = (vec2[1] - vec1[1]) / time
    a = robotWidth / 2
    b = robotLength / 2
    omega = 0
    if np.isclose(vx, 0) and np.isclose(vy, 0):
        theta1 = np.arctan2(vec1[3], vec1[2])
        theta2 = np.arctan2(vec2[3], vec2[2])
        omega = (theta2 - theta1) / time
    fr = round(vy - vx + omega * (a + b), 3)
    fl = round(vy + vx - omega * (a + b), 3)
    rl = round(vy - vx - omega * (a + b), 3)
    rr = round(vy + vx + omega * (a + b), 3)
    return fl, fr, rl, rr


def computeTankWheelSpeed(vec1, vec2, time, robotWidth, robotLength):
    vx = 0
    vy = distance(vec1, vec2) / time
    a = robotWidth / 2
    b = robotLength / 2
    theta1 = np.arctan2(vec1[3], vec1[2])
    theta2 = np.arctan2(vec2[3], vec2[2])
    omega = (theta2 - theta1) / time
    fr = round(vy - vx + omega * (a + b), 3)
    fl = round(vy + vx - omega * (a + b), 3)
    rl = round(vy - vx - omega * (a + b), 3)
    rr = round(vy + vx + omega * (a + b), 3)
    return fl, fr, rl, rr


def distance(point1, point2):
    return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


def getWheelPower(desiredMPS, index):
    # 60%: fr 156.7, fl 118.3, rr 154.9, rl 142.2
    # 80%: fr 173.3, fl 175.8, rr 161.6, rl 177.7
    # 100%: fr 193.1, fl 195.3, rr 192.3, rl 196.5
    fl = [118.3, 175.8, 195.3]
    fr = [156.7, 173.3, 193.1]
    rl = [142.2, 177.7, 196.5]
    rr = [154.9, 161.6, 192.3]
    multiplier = (0.07 * np.pi) / 60
    mps_known = [
        [x * multiplier for x in fl],
        [x * multiplier for x in fr],
        [x * multiplier for x in rl],
        [x * multiplier for x in rr],
    ]

    pwm_known = [60, 80, 100]

    return round(np.interp(desiredMPS, mps_known[index], pwm_known), 2)
