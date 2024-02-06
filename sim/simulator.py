import matplotlib.pyplot as plt
import numpy as np
from advanced import quad
from advanced import arc
from advanced import tank


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
    pltPoints = []
    for i in range(len(points)):
        ni = nexti(i, len(points))
        if sequences[i] == "line":
            pltPoints.extend(quad.computeQuad(points[i], points[ni], unitPerDot))
        elif sequences[i] == "arc":
            pltPoints.extend(arc.computeArc(points[i], points[ni], degPerDot))

    pltPoints = tank.computeTurns(pltPoints, points, turnDegPerDot)
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


if __name__ == "__main__":
    points = [(7, 6), (1, 0), (7, 0), (1, 6)]
    sequences = ["line", "arc", "line", "arc"]
    unitPerDot = 1
    degPerDot = 30
    turnPerDot = 30
    secPerDot = 1
    robotWidth = 0.220  # in meters
    robotLength = 0.220
    text_position = (0.95, 0.95)

    pltPoints = simulate(points, sequences, unitPerDot, degPerDot, turnPerDot)
    fig, ax = plt.subplots()
    plotSetup(
        ax,
        min(pltPoints, key=lambda x: x[0])[0],
        max(pltPoints, key=lambda x: x[0])[0],
        min(pltPoints, key=lambda x: x[1])[1],
        max(pltPoints, key=lambda x: x[1])[1],
    )

    text_annotation = ax.text(
        *text_position,
        "",
        fontsize=12,
        ha="right",
        va="top",
        transform=ax.transAxes,
    )

    for i in range(len(pltPoints)):
        color = plt.cm.viridis(pltPoints[i][2])
        ax.quiver(
            pltPoints[i][0],
            pltPoints[i][1],
            pltPoints[i][2],
            pltPoints[i][3],
            color=color,
        )
        text_content = "FL: %.3f\nFR: %.3f\nRL: %.3f\nRR: %.3f" % computeWheelSpeed(
            pltPoints[i], pltPoints[nexti(i, len(pltPoints))], robotWidth, robotLength
        )
        text_annotation.set_text(text_content)
        plt.pause(secPerDot)
    plt.show()
