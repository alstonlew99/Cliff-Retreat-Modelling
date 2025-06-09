import json
import numpy as np
import matplotlib.pyplot as plt

with open('config.json', 'r') as f:
    config = json.load(f)
SLOPE = config['SLOPE']

# set up the geometry where Z is elevation and X is cross-shore distance
Z = np.arange(-10., 10., 0.1)
X = Z / SLOPE

# find sea level
SLInd = np.argmin(np.abs(0. - Z))

# set up a figure and set of axes for plotting
fig1, ax1 = plt.subplots()

# plot the platform and mean sea level at 0m
ax1.plot(X, Z, 'k-')
ax1.plot([X[0], X[SLInd]], [0, 0], 'b--')
ax1.set_xlabel("Distance (m)")
ax1.set_ylabel("Elevation (m)")

# Optional: control aspect ratio
# ax1.axis('equal')
# ax1.set_aspect(10.)

plt.show()

""" SET THE WAVE HEIGHT HERE """
WAVEHEIGHT = config['WAVEHEIGHT']

# calculate water depth and find breaking point
WaterDepth = 0-Z[0:SLInd]
BreakingPoint = np.argmin(np.abs(WaterDepth-WAVEHEIGHT*0.8))

#plot the breaking point
ax1.plot([X[BreakingPoint],X[BreakingPoint]],[-WaterDepth[BreakingPoint],0],'r-')
fig1