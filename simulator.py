import matplotlib.pyplot as plt
import quad
import arc


def plotSetup(minx, maxx, miny, maxy):
    fig, ax = plt.subplots()
    ax.set(xlim=[minx, maxx], ylim=[miny, maxy])
    return fig, ax


if __name__ == "__main__":
    points = [(2, 5), (5, 2), (3, 0), (1, 4)]
    unitPerDot = 1
    degPerDot = 10
    secPerDot = 0.1
    arcs = []

    arcs.extend(quad.computeQuad(points[0], points[1], unitPerDot))
    arcs.extend(arc.computeArc(points[1], points[2], degPerDot))
    arcs.extend(quad.computeQuad(points[2], points[3], unitPerDot))
    arcs.extend(arc.computeArc(points[3], points[0], degPerDot))

    _, ax = plotSetup(min(arcs, key=lambda x: x[0])[0],
                      max(arcs, key=lambda x: x[0])[0],
                      min(arcs, key=lambda x: x[1])[1],
                      max(arcs, key=lambda x: x[1])[1])

    for point in arcs:
        ax.plot(point[0], point[1], 'ro')
        plt.pause(secPerDot)
    plt.show()
