# The main class tying together the full cliff retreat simulation.
# It integrates geometry, tides, erosion, tectonics, and plotting modules.

import numpy as np
from rockcoast.geometry import initialize_topography
from rockcoast.tidal import generate_tide_series, compute_weathering_efficacy
from rockcoast.erosion import compute_wave_force, apply_erosion
from rockcoast.tectonics import apply_earthquake
from rockcoast.plotting import setup_plots, update_profile_plot, finalize_plots

class CliffRetreatModel:
    def __init__(self, config):
        # load parameters from config dict
        self.ZMin=config["ZMin"]
        self.ZMax=config["ZMax"]
        self.dz=config["dz"]
        self.InitialSlope=config["InitialSlope"]
        self.TidalRange=config["TidalRange"]
        self.MaxWeatheringEfficacy=config["MaxWeatheringEfficacy"]
        self.WaveHeight=config["WaveHeight"]
        self.WaveDecayCoef=config["WaveDecayCoef"]
        self.MaxResistance=config["MaxResistance"]
        self.EarthquakeInterval=config["EarthquakeInterval"]
        self.UpliftAmount=config["UpliftAmount"]
        self.SimulationSteps=config["SimulationSteps"]

        # create geometry
        self.Z, self.X=initialize_topography(self.ZMin, self.ZMax, self.dz, self.InitialSlope)
        self.InitialX=self.X.copy()

        # tidal profile and weathering efficacy
        self.Zw=generate_tide_series(self.TidalRange)
        IntertidalElevations=np.arange(0.5*self.TidalRange, -0.5*self.TidalRange- 1e-6,-self.dz)
        self.WeatheringEfficacy=compute_weathering_efficacy(IntertidalElevations, self.TidalRange, self.MaxWeatheringEfficacy)

        # vertical index ranges for erosion
        self.HighTideInd=np.argmin(np.abs(self.Z-0.5*self.TidalRange))
        self.LowTideInd=np.argmin(np.abs(self.Z+0.5*self.TidalRange))

        # initialize resistance profile
        self.Resistance=np.ones(len(self.Z))*self.MaxResistance

    def run(self):
        # prepare interactive plot
        fig, ax, line=setup_plots(self.Z, self.X)

        for step in range(1, self.SimulationSteps+1):
            print(f"Step {step}/{self.SimulationSteps}: remaining rock={self.Resistance.sum():.1f}")

            # compute wave force
            WaveForce=compute_wave_force(
                self.Zw,
                sea_level=0.,
                Z=self.Z,
                X=self.X,
                wave_height=self.WaveHeight,
                wave_decay_coef=self.WaveDecayCoef,
                HighTideInd=self.HighTideInd
            )

            # apply erosion
            apply_erosion(
                WaveForce,
                self.Resistance,
                self.X,
                self.Z,
                self.LowTideInd,
                self.HighTideInd,
                self.WeatheringEfficacy,
                self.MaxResistance
            )

            # apply earthquake uplift (if applicable)
            self.Z, self.X, self.Resistance=apply_earthquake(
                step,
                self.Z,
                self.X,
                self.Resistance,
                EarthquakeInterval=self.EarthquakeInterval,
                UpliftAmount=self.UpliftAmount,
                ZMax=self.ZMax,
                MaxResistance=self.MaxResistance
            )

            # update vertical index after uplift
            self.HighTideInd=np.argmin(np.abs(self.Z-0.5*self.TidalRange))
            self.LowTideInd=np.argmin(np.abs(self.Z+0.5*self.TidalRange))

            # update animation
            update_profile_plot(line, self.X, self.Z)

        # plot retreat distance
        finalize_plots(self.Z, self.X, self.InitialX)
