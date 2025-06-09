import json
import numpy as np
import matplotlib.pyplot as plt


'''
Waves
'''
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


""" Wave Breaking """
WAVEHEIGHT = config['WAVEHEIGHT']

# calculate water depth and find breaking point
WaterDepth = 0-Z[0:SLInd]
BreakingPoint = np.argmin(np.abs(WaterDepth-WAVEHEIGHT*0.8))

#plot the breaking point
ax1.plot([X[BreakingPoint],X[BreakingPoint]],[-WaterDepth[BreakingPoint],0],'r-')
fig1

""" WAVE DECAY"""
DECAY_COEFFICIENT = config['DECAY_COEFFICIENT']
COLOUR = 'b'

# calculate wave heights
H = np.zeros(SLInd)
H[0:BreakingPoint] = WAVEHEIGHT
H[BreakingPoint:] = WAVEHEIGHT*np.exp(-(X[BreakingPoint:SLInd]-X[BreakingPoint])*DECAY_COEFFICIENT)

# set up a figure and set of axes for plotting
fig2, ax2 = plt.subplots()

ax2.plot(X[0:SLInd],H,'-',color=COLOUR)
ax2.set_xlabel("Distance (m)")
ax2.set_ylabel("Wave Height (m)")
ax2.set_xlim(X[BreakingPoint]-10.,X[SLInd]+10.)


# execute the exponential equation again here for the breaking wave
H[BreakingPoint:] = WAVEHEIGHT*np.exp(-(X[BreakingPoint:SLInd]-X[BreakingPoint])*DECAY_COEFFICIENT)



