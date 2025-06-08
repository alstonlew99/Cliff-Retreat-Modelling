# This module computes the wave force and erosion application.

import numpy as np

def compute_wave_force(Zw, sea_level, Z, X, wave_height, wave_decay_coef, HighTideInd):
    """
    Calculate the wave force distribution along the cliff profile.

    Parameters:
    - Zw (numpy.ndarray): array of tide levels during wave cycle
    - sea_level (float): current sea level
    - Z (numpy.ndarray): vertical profile
    - X (numpy.ndarray): horizontal profile
    - wave_height (float): maximum wave height
    - wave_decay_coef (float): exponential decay rate of wave energy with depth
    - HighTideInd (int): index of high tide position in Z

    Returns:
    - WaveForce (numpy.ndarray): cumulative wave force per elevation step
    """
    # find position of breaking point
    BreakingPoint=sea_level-wave_height/2.

    # number of waves per elevation cell
    Waves=np.zeros(len(Z))
    for i in range(len(Zw)):
        # find the index in Z that matches the current wave elevation
        BreakingInd=np.argmin(np.abs(sea_level+Zw[i]-Z))
        Waves[BreakingInd]+=1.

    # wave energy decay with distance inland
    Depth=Z[HighTideInd]-Z
    DecayFactor=np.exp(-wave_decay_coef*Depth)

    # combine to get wave force
    WaveForce=Waves*DecayFactor
    return WaveForce

def apply_erosion(WaveForce, Resistance, X, Z, LowTideInd, HighTideInd, WeatheringEfficacy, MaxResistance):
    """
    Apply erosion to the profile based on wave force and weathering within the intertidal zone.

    Parameters:
    - WaveForce (numpy.ndarray): force from waves at each elevation
    - Resistance (numpy.ndarray): remaining resistance of each cell
    - X (numpy.ndarray): horizontal cliff profile
    - Z (numpy.ndarray): vertical elevation profile
    - LowTideInd (int): index of low tide position
    - HighTideInd (int): index of high tide position
    - WeatheringEfficacy (numpy.ndarray): relative erosion weight per elevation (from tidal.py)
    - MaxResistance (float): baseline maximum resistance value
    """
    for i in range(LowTideInd, HighTideInd):
        # reduce resistance
        Resistance[i]-=WaveForce[i]+WeatheringEfficacy[i]
        if Resistance[i]<0:
            Resistance[i]=MaxResistance
            X[i]+=1.
