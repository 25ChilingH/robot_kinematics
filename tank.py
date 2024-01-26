import numpy as np
import simulator


def computeArrow(arcs):
    angles = []
    for i in range(len(arcs)):
        nexti = simulator.nexti(i, len(arcs))
        point1 = tuple(arcs[i])
        point2 = tuple(arcs[nexti])
        angles.append([point1, np.arctan2(point2[1] - point1[1],
                                          point2[0] - point1[0])])
    return angles


def computeTurns(plotpoints, points, degPerTurn):
    angles = computeArrow(plotpoints)
    arcs = []
    for i in range(len(angles)):
        nexti = simulator.nexti(i, len(angles))
        arcs.append([angles[i][0][0], angles[i][0][1],
                     np.cos(angles[i][1]), np.sin(angles[i][1])])
        if simulator.pointInArray(angles[nexti][0], points):
            if angles[i][1] < angles[nexti][1]:
                step = np.deg2rad(degPerTurn)
            else:
                step = -np.deg2rad(degPerTurn)
            for theta in np.arange(angles[i][1], angles[nexti][1], step):
                arcs.append([angles[nexti][0][0], angles[nexti][0][1],
                             np.cos(theta), np.sin(theta)])
    return arcs
