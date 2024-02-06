"""
by-wheel speed display utility for car movement

Revision History:
Version: date: changes:
         Feb 9  converted to function
"""
__version__ = '0.2'
__date__ = 'Feb 9, 2023'
__author__ = 'Martin Baynes'

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
import simulator

# equivalent of Arduino map()
def valmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


# plot_wheels(graphs, wheelSpeed, maxSpeed, radius):
# use adk[0] for car's path plot
def plot_wheels(axd, wheelName, wheelSpeed, maxSpeed, radius=1):
    for idx, k in enumerate(axd):
        if idx > 0:
            ang = valmap(wheelSpeed[idx-1], -maxSpeed, maxSpeed, np.pi, 0)
            dx = radius * math.cos(ang)
            dy = radius * math.sin(ang)
            axd[k].clear()
            axd[k].set(xlim=(-1.5, 1.5),  xticks=[], yticks=[],
                       ylim=(-1.5, 1.5))
            axd[k].annotate(wheelName[idx - 1], (0.1, 0.5),
                            xycoords='axes fraction', va='center')
            axd[k].quiver(0, 0, dy, dx, width=0.04,
                          pivot='mid', angles='uv',
                          scale_units='height', scale=2)
            axd[k].annotate(wheelSpeed[idx - 1], (.8, 0.5),
                            xycoords='axes fraction', va='center')


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

    pltPoints = simulator.simulate(points, sequences, unitPerDot, degPerDot, turnPerDot)

    fig, axd = plt.subplot_mosaic([['left', 'left', 'upper middle', 'upper right'],
                                ['left', 'left', 'lower middle', 'lower right']
                                ], figsize=(8, 4), layout="constrained")
    simulator.plotSetup(
        axd['left'],
        min(pltPoints, key=lambda x: x[0])[0],
        max(pltPoints, key=lambda x: x[0])[0],
        min(pltPoints, key=lambda x: x[1])[1],
        max(pltPoints, key=lambda x: x[1])[1],
    )
    fig.suptitle('Simulator with wheel speed display')
    plt.style.use('_mpl-gallery-nogrid')
    wheelName = ['fl', 'fr', 'rl', 'rr']

    interactive(True)

    maxSpeed = 2
    for i in range(len(pltPoints)):
        color = plt.cm.viridis(pltPoints[i][2])
        axd['left'].quiver(
            pltPoints[i][0],
            pltPoints[i][1],
            pltPoints[i][2],
            pltPoints[i][3],
            color=color,
        )
        wheelSpeeds = simulator.computeWheelSpeed(
            pltPoints[i], pltPoints[simulator.nexti(i, len(pltPoints))], robotWidth, robotLength
        )
        plot_wheels(axd, wheelName, wheelSpeeds, maxSpeed)
        plt.pause(secPerDot)
    
    plt.show()
    bye = input('press enter key to end: ')
    print('Bye')
