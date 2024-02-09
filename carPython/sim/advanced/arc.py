import matplotlib.pyplot as plt
import numpy as np
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils import distance
from utils import plotSetup


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


def arc():
    points = [(5, 5), (3, 0)]
    degPerDot = 10
    secPerDot = 0.1
    arcs = []
    for i in range(len(points) - 1):
        arcs.extend(computeArc(points[i], points[i + 1], degPerDot))

    fig, ax = plt.subplots()
    plotSetup(
        ax,
        min(arcs, key=lambda x: x[0])[0],
        max(arcs, key=lambda x: x[0])[0],
        min(arcs, key=lambda x: x[1])[1],
        max(arcs, key=lambda x: x[1])[1],
    )

    for point in arcs:
        ax.plot(point[0], point[1], "ro")
        plt.pause(secPerDot)
    plt.show()


if __name__ == "__main__":
    arc()
