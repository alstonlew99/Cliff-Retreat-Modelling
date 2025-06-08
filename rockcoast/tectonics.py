# This module implements tectonic uplift caused by earthquakes.

import numpy as np

def apply_earthquake(step, Z, X, Resistance, EarthquakeInterval, UpliftAmount, ZMax, MaxResistance):
    """
Apply tectonic uplift to the coastal profile every EarthquakeInterval years.

    Parameters:
    - step (int): current simulation year
    - Z (numpy.ndarray): vertical elevation profile
    - X (numpy.ndarray): horizontal cliff face positions
    - Resistance (numpy.ndarray): resistance at each elevation cell
    - EarthquakeInterval (int): frequency of earthquakes (in years)
    - UpliftAmount (float): elevation added per earthquake
    - ZMax (float): maximum vertical model extent (top boundary)
    - MaxResistance (float): maximum rock resistance value

    Returns:
    - Z (numpy.ndarray): updated elevation profile
    - X (numpy.ndarray): updated horizontal profile
    - Resistance (numpy.ndarray): updated resistance profile
    """
    if (step%EarthquakeInterval)==0:
        # Uplift profile
        Z=Z+UpliftAmount

        # remove cells that are now above model domain
        InDomain=np.where(Z<=ZMax)[0]
        Z=Z[InDomain]
        X=X[InDomain]
        Resistance=Resistance[InDomain]

        # Add new cells at base
        ZMin=Z.min()
        NewZ=np.arange(ZMin-UpliftAmount, ZMin, Z[1]-Z[0])
        Z=np.concatenate((NewZ, Z))

        # extend X and Resistance accordingly
        NewX=np.ones(len(NewZ))*X[0]
        NewResistance=np.ones(len(NewZ))*MaxResistance
        X=np.concatenate((NewX, X))
        Resistance=np.concatenate((NewResistance, Resistance))

    return Z, X, Resistance
