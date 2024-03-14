from scipy.interpolate import CubicSpline
import numpy as np
import matplotlib.pyplot as plt


def plotObstacle():
    plt.hlines(
        y=[2.5, 3.0, 2.75, 2.0],
        xmin=[0.0025, 1.1, 0.6, 0.4],
        xmax=[0.2, 1.25, 1.0, 0.6],
        color="g",
    )
    plt.vlines(
        x=[0.2, 0.4, 0.6, 1.0, 1.1],
        ymin=[2.5, 1.0, 2.0, 1.0, 3.0],
        ymax=[4.0, 2.0, 2.75, 2.75, 4.0],
        color="g",
    )


def spline():
    x = [0, 0.5, 0.95, 1.25]
    y = [1, 3, 3.5, 1]

    # use bc_type = 'natural' adds the constraints as we described above
    f = CubicSpline(x, y, bc_type="natural")
    x_new = np.linspace(min(x), max(x), 100)
    y_new = f(x_new)

    plt.figure(figsize=(10, 8))
    plt.plot(x_new, y_new, "b")
    plt.plot(x, y, "ro")
    plotObstacle()
    plt.title("Cubic Spline Interpolation")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


if __name__ == "__main__":
    spline()
