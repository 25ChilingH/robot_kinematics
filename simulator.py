import matplotlib.pyplot as plt
import numpy as np
import quad
import arc
import tank


def plotSetup(minx, maxx, miny, maxy):
    padding = max((maxx-minx)//3, (maxy-miny)//3)
    fig, ax = plt.subplots()
    ax.set(xlim=[minx - padding, maxx + padding],
           ylim=[miny - padding, maxy + padding])
    return fig, ax


def nexti(i, length):
    return (i + 1) % length


def pointInArray(point, arrayOfPoints):
    for pt in arrayOfPoints:
        if np.isclose(point, pt)[0] and np.isclose(point, pt)[1]:
            return True
    return False


if __name__ == "__main__":
    points = [(1, 6), (7, 6), (7, 0), (1, 0)]
    unitPerDot = 1
    degPerDot = 30
    secPerDot = 0.5
    arcs = []

    arcs.extend(quad.computeQuad(points[0], points[1], unitPerDot))
    arcs.extend(arc.computeArc(points[1], points[2], degPerDot))
    arcs.extend(quad.computeQuad(points[2], points[3], unitPerDot))
    arcs.extend(arc.computeArc(points[3], points[0], degPerDot))

    _, ax = plotSetup(min(arcs, key=lambda x: x[0])[0],
                      max(arcs, key=lambda x: x[0])[0],
                      min(arcs, key=lambda x: x[1])[1],
                      max(arcs, key=lambda x: x[1])[1])

    turns = tank.computeTurns(arcs, points, 30)

    for i in range(len(turns)):
        color = plt.cm.viridis(turns[i][2])
        ax.quiver(turns[i][0], turns[i][1],
                  turns[i][2], turns[i][3], color=color)
        plt.pause(secPerDot)
    plt.show()
