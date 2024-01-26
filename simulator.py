import matplotlib.pyplot as plt
import numpy as np
import sim.quad as quad
import sim.arc as arc
import sim.tank as tank


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


def simulate(points, sequences, unitPerDot,
             degPerDot, turnDegPerDot, secPerDot):
    arcs = []
    for i in range(len(points)):
        ni = nexti(i, len(points))
        if sequences[i] == "line":
            arcs.extend(quad.computeQuad(points[i], points[ni], unitPerDot))
        elif sequences[i] == "arc":
            arcs.extend(arc.computeArc(points[i], points[ni], degPerDot))

    _, ax = plotSetup(min(arcs, key=lambda x: x[0])[0],
                      max(arcs, key=lambda x: x[0])[0],
                      min(arcs, key=lambda x: x[1])[1],
                      max(arcs, key=lambda x: x[1])[1])

    arcs = tank.computeTurns(arcs, points, turnDegPerDot)

    for i in range(len(arcs)):
        color = plt.cm.viridis(arcs[i][2])
        ax.quiver(arcs[i][0], arcs[i][1],
                  arcs[i][2], arcs[i][3], color=color)
        plt.pause(secPerDot)
    plt.show()


if __name__ == "__main__":
    points = [(7, 6), (1, 0), (7, 0), (1, 6)]
    sequences = ["line", "arc", "line", "arc"]
    unitPerDot = 1
    degPerDot = 30
    turnPerDot = 30
    secPerDot = 0.5

    simulate(points, sequences, unitPerDot, degPerDot, turnPerDot, secPerDot)
