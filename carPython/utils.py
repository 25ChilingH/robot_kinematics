import numpy as np
from simple_pid import PID


def plotSetup(ax, minx, maxx, miny, maxy):
    ax.set(xlim=[minx - 1, maxx + 1], ylim=[miny - 1, maxy + 1])


def nexti(i, length):
    return (i + 1) % length


def pointInArray(point, arrayOfPoints):
    for pt in arrayOfPoints:
        if np.isclose(point, pt)[0] and np.isclose(point, pt)[1]:
            return True
    return False


def allZeroArray(arr):
    return np.any(np.absolute(arr) < 1e-1)

def initPIDController():
    kP = 0.7
    kI = 0
    kD = 0.0
    pid = PID(kP, kI, kD)
    return pid

def computePltPoints(points, sequences, unitPerDot, degPerDot, drive, turnDegPerDot):
    pltPoints = []
    for i in range(len(sequences)):
        ni = nexti(i, len(points))
        if sequences[i] == "line":
            pltPoints.extend(computeQuad(points[i], points[ni], unitPerDot))
        elif sequences[i] == "arc":
            pltPoints.extend(computeArc(points[i], points[ni], degPerDot))
    vecs = computeVectors(pltPoints)
    pltPoints = computeCornerTurns(vecs, points, drive, turnDegPerDot)
    return pltPoints


def computeVectors(arcs):
    angles = []
    for i in range(len(arcs)):
        nextIdx = nexti(i, len(arcs))
        point1 = tuple(arcs[i])
        point2 = tuple(arcs[nextIdx])
        angles.append(
            [point1, np.arctan2(point2[1] - point1[1], point2[0] - point1[0])]
        )
    return angles


def computeCornerTurns(angles, points, drive, degPerTurn):
    arcs = []
    for i in range(len(angles) - 1):
        nextIdx = nexti(i, len(angles))
        arcs.append(
            [
                angles[i][0][0],
                angles[i][0][1],
                np.cos(angles[i][1]),
                np.sin(angles[i][1]),
            ]
        )
        if drive == "tank":
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
    print("vx", vx, "vy", vy, "pt 1", vec1, "pt 2", vec2)
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


def rotsToMeters():
    return 0.07 * np.pi


def getWheelPower(desiredMPS, index):
    fl = [-194.5, -170.2, -144.6, 0, 145.3, 175.8, 195.3]
    fr = [-195.1, -172.8, -148.7, 0, 146.7, 173.3, 193.1]
    rl = [-194.9, -173.2, -140.1, 0, 144.2, 177.7, 196.5]
    rr = [-193.9, -172.5, -146.4, 0, 144.9, 171.6, 192.3]
    multiplier = rotsToMeters() / 60
    mps_known = [
        [x * multiplier for x in fl],
        [x * multiplier for x in fr],
        [x * multiplier for x in rl],
        [x * multiplier for x in rr],
    ]

    pwm_known = [-100, -60, -80, 0, 60, 80, 100]

    return round(np.interp(desiredMPS, mps_known[index], pwm_known), 2)
