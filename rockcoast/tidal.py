# This module defines the tidal elevation profile and intertidal weathering efficacy.

import numpy as np

def generate_tide_series(tidal_range):
    """
    Create a synthetic tide signal to represent the spatial distribution of wave attack.
    This is used as a sampling distribution across the profile to simulate the spatial
    impact of waves within a typical tidal cycle.

    Parameters:
    - tidal_range (float): the total vertical range of the tide (in metres)

    Returns:
    - Zw (numpy.ndarray): vertical distribution of tidal wave impact positions
    """
    # create tidal water levels
    TideTime=np.arange(0, 24., 0.1)
    Zw=0.5*tidal_range*np.sin(TideTime*2.*np.pi/12.)
    return Zw

def compute_weathering_efficacy(intertidal_elevations, tidal_range, max_weathering_efficacy):
    """
    Define the distribution of weathering rates within the intertidal zone.

    This function applies a Gaussian distribution centred at 0.25*TidalRange,
    mimicking where bio-erosion or wetting-drying cycles are most effective.

    Parameters:
    - intertidal_elevations (numpy.ndarray): array of elevation values within the intertidal zone
    - tidal_range (float): total vertical tidal range (in metres)
    - max_weathering_efficacy (float): peak weathering efficacy coefficient

    Returns:
    - WeatheringEfficacy (numpy.ndarray): efficacy values at each elevation, flipped to match Z array
    """
    WeatheringEfficacy=np.zeros(len(intertidal_elevations))

    # find the location of the maximum weathering rate
    MaxWeatheringInd=np.argmin(np.abs(intertidal_elevations - 0.25 * tidal_range))

    # calculate the distribution of weathering rates
    WeatheringEfficacy[0:MaxWeatheringInd]=max_weathering_efficacy*np.exp(-((intertidal_elevations[0:MaxWeatheringInd]-0.25*tidal_range)**2.)/(0.1*0.25*tidal_range))
    WeatheringEfficacy[MaxWeatheringInd:]=max_weathering_efficacy*np.exp(-(0.25*tidal_range - intertidal_elevations[MaxWeatheringInd:])**2./(0.25*tidal_range))

    # invert order so it matches increasing elevation upward
    return WeatheringEfficacy[::-1]
