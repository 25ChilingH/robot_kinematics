import matplotlib.pyplot as plt
import numpy as np

r = 1
center = (0, 0)
degPerDot = 10
secPerDot = 1

fig, ax = plt.subplots()
ax.set(xlim=[-r + center[0], r + center[0]],
       ylim=[-r + center[1], r + center[1]])

for theta in np.arange(0, 2 * np.pi, np.deg2rad(degPerDot)):
    x = center[0] + r * np.cos(theta)
    y = center[1] + r * np.sin(theta)
    ax.plot(x, y, 'ro')
    plt.pause(secPerDot)

plt.show()
