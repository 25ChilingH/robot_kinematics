"""
by-wheel speed display utility for car movement

Revision History:
Version: date: changes:
         Feb 9  converted to function
"""

__version__ = "0.2"
__date__ = "Feb 9, 2023"
__author__ = "Martin Baynes"

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
import utils
import main


# equivalent of Arduino map()
def valmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


# plot_wheels(graphs, wheelSpeed, maxSpeed, radius):
# use adk[0] for car's path plot
def plot_wheels(axd, wheelName, wheelSpeed, maxSpeed, radius=1):
    for idx, k in enumerate(axd):
        if idx > 0:
            ang = valmap(wheelSpeed[idx - 1], -maxSpeed, maxSpeed, np.pi, 0)
            dx = radius * math.cos(ang)
            dy = radius * math.sin(ang)
            axd[k].clear()
            axd[k].set(xlim=(-1.5, 1.5), xticks=[], yticks=[], ylim=(-1.5, 1.5))
            axd[k].annotate(
                wheelName[idx - 1], (0.1, 0.5), xycoords="axes fraction", va="center"
            )
            axd[k].quiver(
                0,
                0,
                dy,
                dx,
                width=0.04,
                pivot="mid",
                angles="uv",
                scale_units="height",
                scale=2,
            )
            axd[k].annotate(
                wheelSpeed[idx - 1], (0.8, 0.5), xycoords="axes fraction", va="center"
            )


if __name__ == "__main__":

    fig, axd = plt.subplot_mosaic(
        [
            ["left", "left", "upper middle", "upper right"],
            ["left", "left", "lower middle", "lower right"],
        ],
        figsize=(8, 4),
        layout="constrained",
    )
    utils.plotSetup(
        axd["left"],
        min(main.pltPoints, key=lambda x: x[0])[0],
        max(main.pltPoints, key=lambda x: x[0])[0],
        min(main.pltPoints, key=lambda x: x[1])[1],
        max(main.pltPoints, key=lambda x: x[1])[1],
    )
    fig.suptitle("Simulator with wheel speed display")
    plt.style.use("_mpl-gallery-nogrid")
    wheelName = ["fl", "fr", "rl", "rr"]

    interactive(True)

    maxSpeed = main.unitPerDot / main.delay

    for i in range(len(main.pltPoints)):
        color = plt.cm.viridis(main.pltPoints[i][2])
        axd["left"].quiver(
            main.pltPoints[i][0],
            main.pltPoints[i][1],
            main.pltPoints[i][2],
            main.pltPoints[i][3],
            color=color,
        )
        wheelSpeeds = utils.computeTankWheelSpeed(
            main.pltPoints[i],
            main.pltPoints[utils.nexti(i, len(main.pltPoints))],
            main.delay,
            main.robotWidth,
            main.robotLength,
        )
        plot_wheels(axd, wheelName, wheelSpeeds, maxSpeed)
        plt.pause(main.delay)

    plt.show()
    bye = input("press enter key to end: ")
    print("Bye")
