import matplotlib.pyplot as plt
import numpy as np
import simulator


def computeQuad(point1, point2, unitPerDot):
    arcs = []
    angle = np.arctan2(point2[1] - point1[1], point2[0] - point1[0])
    dist = np.sqrt((point2[0] - point1[0]) ** 2 +
                   (point2[1] - point1[1]) ** 2)

    x = point1[0]
    y = point1[1]
    for i in np.arange(0, dist, unitPerDot):
        arcs.append([x, y])
        x += np.cos(angle) * unitPerDot
        y += np.sin(angle) * unitPerDot
    return arcs


def quad():
    points = [(2, 5), (5, 2), (3, 0), (1, 4)]
    unitPerDot = 1
    secPerDot = 0.1
    arcs = []
    for i in range(len(points)):
        nexti = simulator.nexti(i, len(points))
        arcs.extend(computeQuad(points[i], points[nexti], unitPerDot))

    _, ax = simulator.plotSetup(min(arcs, key=lambda x: x[0])[0],
                                max(arcs, key=lambda x: x[0])[0],
                                min(arcs, key=lambda x: x[1])[1],
                                max(arcs, key=lambda x: x[1])[1])

    for point in arcs:
        ax.plot(point[0], point[1], 'ro')
        plt.pause(secPerDot)
    plt.show()

if __name__ == "__main__":
    quad()
