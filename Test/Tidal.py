import json
import numpy as np
import matplotlib.pyplot as plt

with open('../rockcoast/config.json', 'r') as f:
    config = json.load(f)
# set up the geometry wher Z is elevation and X is cross-shore distance
SLOPE = config['SLOPE']
Z = np.arange(-10.,10.,0.1)
X = Z/SLOPE
SLInd = np.argmin(np.abs(0.-Z))

""" SET THE TIDAL RANGE HERE (in metres) """
TIDAL_RANGE = config['TIDAL_RANGE']

# set up time vector and apply sine wave to show the tide.
time = np.arange(0,24.,0.01)
Zw = 0.5*TIDAL_RANGE*np.sin(time*2.*np.pi/12.)

# set up a figure and set of axes for plotting
fig3, ax3 = plt.subplots()

# plot a tidal wave over a single day
ax3.plot(time,Zw,'b-')
ax3.set_xlabel("Time (hours)")
ax3.set_ylabel("Water level (m)")

fig4, ax4 = plt.subplots()
ax4.hist(Zw, bins=20, orientation='horizontal', density=True)
ax4.set_xlabel("Relative tidal duration (no units)")
ax4.set_ylabel("Water level (m)")

WAVEHEIGHT = config['WAVEHEIGHT']
DECAY_COEFFICIENT = config['DECAY_COEFFICIENT']

# set up an array to collect wave energy in
CumulativeWaveHeight = np.zeros(len(Z))

# reset water levels incase change of wave height
Zw = 0.5 * TIDAL_RANGE * np.sin(time * 2. * np.pi / 12.)

# set up a loop to consider each water level in the progressive position of the tide in turn
for WaterLevel in Zw:
    # find water level
    WaterLevelInd = np.argmin(np.abs(WaterLevel - Z))

    # calculate water depth and find breaking point
    WaterDepth = WaterLevel - Z[0:WaterLevelInd]
    BreakingPoint = np.argmin(np.abs(WaterDepth - WAVEHEIGHT * 0.8))

    # calculate wave height from this point towards the coast
    H = np.zeros(len(Z))
    H[BreakingPoint:] = WAVEHEIGHT * np.exp(-(X[BreakingPoint:] - X[BreakingPoint]) * DECAY_COEFFICIENT)

    # update the total wave energy array
    CumulativeWaveHeight += H

NormedWaveEnergy = CumulativeWaveHeight / np.max(CumulativeWaveHeight)

# find high and low tide positions
LowTideInd = np.argmin(np.abs(-0.5 * TIDAL_RANGE - Z))
HighTideInd = np.argmin(np.abs(0.5 * TIDAL_RANGE - Z))

# plot the results
fig5, ax5 = plt.subplots()

# plot the platform and mean sea level at 0m
ax5.plot(X, Z, 'k-')
ax5.plot([X[0], X[SLInd]], [0, 0], 'b--')
ax5.plot([X[0], X[LowTideInd]], [-0.5 * TIDAL_RANGE, -0.5 * TIDAL_RANGE], 'b:')
ax5.plot([X[0], X[HighTideInd]], [0.5 * TIDAL_RANGE, 0.5 * TIDAL_RANGE], 'b:')
ax5.set_xlabel("Distance (m)")
ax5.set_ylabel("Elevation (m)")

sc = ax5.scatter(X, Z, s=NormedWaveEnergy * 100., c=CumulativeWaveHeight, zorder=10)
cbar = plt.colorbar(sc)
cbar.set_label("Relative Wave Energy (m)")

ax5.set_xlim(-200, 100)
plt.show()
