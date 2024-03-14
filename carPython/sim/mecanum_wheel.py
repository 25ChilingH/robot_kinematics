import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
import utils
from Robot import Robot

robot = Robot()


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

            axd[k].annotate(
                utils.getWheelPower(wheelSpeed[idx - 1], idx - 1),
                (0.5, 0.8),
                xycoords="axes fraction",
                va="center",
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
        min(robot.pltPoints, key=lambda x: x[0])[0],
        max(robot.pltPoints, key=lambda x: x[0])[0],
        min(robot.pltPoints, key=lambda x: x[1])[1],
        max(robot.pltPoints, key=lambda x: x[1])[1],
    )
    fig.suptitle("Simulator with wheel speed display")
    plt.style.use("_mpl-gallery-nogrid")
    wheelName = ["fl", "fr", "rl", "rr"]

    interactive(True)

    maxSpeed = robot.unitPerDot / robot.delay

    for i in range(len(robot.pltPoints)):
        color = plt.cm.viridis(robot.pltPoints[i][2])
        if robot.drive == "tank":
            axd["left"].quiver(
                robot.pltPoints[i][0],
                robot.pltPoints[i][1],
                robot.pltPoints[i][2],
                robot.pltPoints[i][3],
                color=color,
            )
            wheelSpeeds = utils.computeTankWheelSpeed(
                robot.pltPoints[i],
                robot.pltPoints[utils.nexti(i, len(robot.pltPoints))],
                robot.delay,
                robot.robotWidth,
                robot.robotLength,
            )
        elif robot.drive == "mecanum":
            axd["left"].quiver(robot.pltPoints[i][0], robot.pltPoints[i][1], 0, 1)
            wheelSpeeds = utils.computeWheelSpeed(
                robot.pltPoints[i],
                robot.pltPoints[utils.nexti(i, len(robot.pltPoints))],
                robot.delay,
                robot.robotWidth,
                robot.robotLength,
            ) 
        plot_wheels(axd, wheelName, wheelSpeeds, maxSpeed)
        plt.pause(robot.delay)

    plt.show()
    bye = input("press enter key to end: ")
    print("Bye")
