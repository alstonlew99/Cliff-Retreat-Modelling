# This module sets up the initial spatial domain for the rock coast model.
import numpy as np

def initialize_topography(ZMin, ZMax, dz, InitialSlope):
    """
    Initialize the model domain in cross-section.
    The topography is represented as a horizontal stack of bars of rock
    """

    """
    Parameters:
    - ZMin: minimum elevation (metres)
    - ZMax: maximum elevation (metres)
    - dz: vertical resolution (metres)
    - InitialSlope: slope of the topography (rise/run)

    Returns:
    - Z: vertical elevation array (1D numpy array)
    - X: horizontal distance array (1D numpy array), computed as Z / slope
    """
    # default spatial domain
    Z=np.arange(ZMin, ZMax, dz)
    X=Z/InitialSlope
    return Z, X
