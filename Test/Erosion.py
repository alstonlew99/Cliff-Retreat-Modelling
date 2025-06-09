import json
import numpy as np
import matplotlib.pyplot as plt

with open('../rockcoast/config.json', 'r') as f:
    config = json.load(f)
TIDAL_RANGE=config['TIDAL_RANGE']

# set up intertidal elevations
IntertidalElevations = np.arange(0.5*TIDAL_RANGE,-0.5*TIDAL_RANGE-0.000001,-TIDAL_RANGE/100.)
WeatheringEfficacy = np.zeros(len(IntertidalElevations))

# find the location of the maximimum weathering rate
MaxWeatheringInd = np.argmin(np.abs(IntertidalElevations-0.25*TIDAL_RANGE))

#calculate the distribution of weathering rates
WeatheringEfficacy[0:MaxWeatheringInd] = np.exp(-((IntertidalElevations[0:MaxWeatheringInd]-0.25*TIDAL_RANGE)**2.)/(0.1*0.25*TIDAL_RANGE))
WeatheringEfficacy[MaxWeatheringInd:] = np.exp(-(0.25*TIDAL_RANGE-IntertidalElevations[MaxWeatheringInd:])**2./(0.25*TIDAL_RANGE))

# set up a new figure
fig6, ax6 = plt.subplots(figsize=(4,6))
ax6.plot(WeatheringEfficacy, IntertidalElevations, 'k-')
ax6.set_xlabel("Relative weathering efficacy")
ax6.set_ylabel("Intertidal elevation (m)")
ax6.set_ylim(-0.5*TIDAL_RANGE,0.5*TIDAL_RANGE)