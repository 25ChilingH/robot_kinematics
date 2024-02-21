import matplotlib.pyplot as plt
import sys
import os

parent_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(parent_dir)
import utils

def quad():
    points = [(2, 5), (5, 2), (3, 0), (1, 4)]
    unitPerDot = 1
    secPerDot = 0.1
    arcs = []
    for i in range(len(points)):
        nextIdx = utils.nexti(i, len(points))
        arcs.extend(utils.computeQuad(points[i], points[nextIdx], unitPerDot))

    fig, ax = plt.subplots()
    utils.plotSetup(
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
    quad()
