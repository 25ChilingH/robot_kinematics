import matplotlib.pyplot as plt
import sys
import os

parent_dir = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(parent_dir)
import utils


def arc():
    points = [(5, 5), (3, 0)]
    degPerDot = 10
    secPerDot = 0.1
    arcs = []
    for i in range(len(points) - 1):
        arcs.extend(utils.computeArc(points[i], points[i + 1], degPerDot))

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
    arc()
