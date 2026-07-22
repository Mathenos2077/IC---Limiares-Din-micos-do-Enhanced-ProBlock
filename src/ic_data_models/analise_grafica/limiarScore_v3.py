import numpy as np
import matplotlib.pyplot as plt
import utils

ic = np.linspace(0, 1, 31)
coScoreTotal = np.linspace(0, 1, 31)

IC, COSCORETOTAL = np.meshgrid(ic, coScoreTotal)

Z = utils.getLimiarScore(IC, COSCORETOTAL)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(IC, COSCORETOTAL, Z)
ax.set_xlabel('IC')
ax.set_ylabel('COSCORETOTAL')
ax.set_zlabel('LimiarScore')
plt.show()