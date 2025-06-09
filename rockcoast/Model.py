# import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import rc
rc("font", size=16)
from ipywidgets import FloatProgress
from IPython.display import display
# The main model goes here as a python class
class RockCoast:

    # setup an initialisation function
    # This defines the default variables and parameters for the model
    def __init__(self):

        # default spatial domain
        self.InitialSlope = 1.  # intial conditions
        self.dz = 0.1  # row spacing (metres)
        self.ZMax = 10.  # max elevation (metres)
        self.ZMin = -10.  # min elevation (metres)
        self.Z = np.arange(self.ZMin, self.ZMax, self.dz)
        self.X = self.Z / self.InitialSlope

        # default boundary conditions
        self.WaveHeight = 2.  # wave height (metres)
        self.WaveForceCoef = 10.  # coefficient for efficiency of wave action
        self.TidalRange = 2.  # tidal range (metres)
        self.WaveDecayCoef = 0.1  # (in metres?)
        self.SeaLevel = 0.  # elevation (metres)
        self.SeaLevelRise = 0.  # rate (m/yr)

        # tectonics
        self.EarthquakeUplift = 0.
        self.EarthquakeTime = 1000.
        self.EarthquakeInterval = 1000.

        # resistance and weathering
        self.MaxResistance = 2000.
        self.Resistance = np.ones(len(self.Z)) * self.MaxResistance
        self.MaxWeatheringEfficacy = 100.

        # setup the time control
        self.Time = 0.  # we will start at time 0 (years)
        self.dt = 1.  # time step (y)
        self.EndTime = 1000.  # time the model will stop (y)

        # setup plotting control
        self.PlotFigures = True
        self.PlotTime = 0.
        self.PlotInterval = 100.

    # this function runs the model
    def RunModel(self):

        # Create a progress bar to show the model is working
        f = FloatProgress(min=self.Time, max=self.EndTime)
        display(f)

        # set up a figure for plotting the profile results
        fig1, ax1 = plt.subplots(figsize=(16, 6))
        ax1.set_xlabel("Distance (m)")
        ax1.set_ylabel("Elevation (m)")

        # set up a figure for plotting the profile results
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.set_xlabel("Time (years)")
        ax2.set_ylabel("Retreat Rate (m/y)")

        # some lists for plotting
        Times = []
        Rates = []

        # reset the initial model domain
        self.Z = np.arange(self.ZMin, self.ZMax, self.dz)
        self.X = self.Z / self.InitialSlope

        # set up an array to collect wave energy in
        CumulativeWaveHeight = np.zeros(len(self.Z))

        # create tidal water levels
        TideTime = np.arange(0, 24., 0.1)
        Zw = 0.5 * self.TidalRange * np.sin(TideTime * 2. * np.pi / 12.)

        # set up weathering distribution
        IntertidalElevations = np.arange(0.5 * self.TidalRange, -0.5 * self.TidalRange - 0.000001, -self.dz)
        WeatheringEfficacy = np.zeros(len(IntertidalElevations))

        # find the location of the maximimum weathering rate
        MaxWeatheringInd = np.argmin(np.abs(IntertidalElevations - 0.25 * self.TidalRange))

        # calculate the distribution of weathering rates
        WeatheringEfficacy[0:MaxWeatheringInd] = self.MaxWeatheringEfficacy * np.exp(
            -((IntertidalElevations[0:MaxWeatheringInd] - 0.25 * self.TidalRange) ** 2.) / (
                        0.1 * 0.25 * self.TidalRange))
        WeatheringEfficacy[MaxWeatheringInd:] = self.MaxWeatheringEfficacy * np.exp(
            -(0.25 * self.TidalRange - IntertidalElevations[MaxWeatheringInd:]) ** 2. / (0.25 * self.TidalRange))
        WeatheringEfficacy = WeatheringEfficacy[::-1]

        # loop through time and update hillslope morphology
        while self.Time <= self.EndTime:

            # find high and low tide positions
            LowTideInd = np.argmin(np.abs(self.SeaLevel - 0.5 * self.TidalRange - self.Z))
            HighTideInd = np.argmin(np.abs(self.SeaLevel + 0.5 * self.TidalRange - self.Z))

            # Calculate Total Wave Force impacting the coast over a tidal cycle
            WaveForce = np.zeros(len(self.Z))

            # set up a loop to consider each water level in the progressive position of the tide in turn
            for WaterLevel in Zw:

                # find water level
                WaterLevelInd = np.argmin(np.abs(self.SeaLevel + WaterLevel - self.Z))

                # calculate water depth and find breaking point
                WaterDepth = self.SeaLevel + WaterLevel - self.Z[0:WaterLevelInd]
                try:
                    BreakingPoint = np.argmin(np.abs(WaterDepth - self.WaveHeight * 0.8))
                except:
                    print(WaterLevelInd)

                # calculate wave height from this point towards the coast
                H = np.zeros(len(self.Z))
                H[BreakingPoint:HighTideInd] = self.WaveHeight * np.exp(
                    -(self.X[BreakingPoint:HighTideInd] - self.X[BreakingPoint:HighTideInd]) * self.WaveDecayCoef)

                # update the total wave energy array
                WaveForce += H ** 2.

            # set efficacy of waves
            WaveForce *= self.WaveForceCoef

            # do some intertidal weathering
            for i in range(LowTideInd, HighTideInd):
                self.Resistance[i] -= WeatheringEfficacy[i - LowTideInd]

            for i in range(0, len(self.Z)):
                while WaveForce[i] > self.Resistance[i]:
                    self.X[i] += 0.1
                    WaveForce[i] -= self.Resistance[i]
                    self.Resistance[i] = self.MaxResistance

            # collapse cliff if there is any undercutting
            # find most landward point in intertidal zone
            MaxIntertidalX = np.max(self.X[LowTideInd:HighTideInd])
            MaxIntertidalXInd = LowTideInd + np.argmax(self.X[LowTideInd:HighTideInd])

            for i in range(MaxIntertidalXInd, len(self.X)):
                if self.X[i] < MaxIntertidalX:
                    self.X[i] = MaxIntertidalX

            # plot the model progress
            if self.Time == 0:

                # plot the profile
                ax1.plot(self.X, self.Z, color=cm.coolwarm(self.Time / self.EndTime))
                Times.append(self.PlotTime)
                LastCliffPosition = MaxIntertidalX
                LastTime = self.Time

                # plt.plot(x[i_sealevel],z[i_sealevel],'ro',markersize=10)
                # plt.plot([x[0],x[0]],[z[0],z[0]+5.0],color=[t_ime/t_max,0.5,0.5])

                # update plot time
                self.PlotTime += self.PlotInterval

                # update progress bar
                f.value = self.Time

            elif self.Time >= self.PlotTime:
                # plot the profile
                ax1.plot(self.X, self.Z, color=cm.coolwarm(self.Time / self.EndTime))
                Times.append(self.PlotTime)

                # get rates and update saved position

                Rate = (MaxIntertidalX - LastCliffPosition) / (self.Time - LastTime)
                Rates.append(Rate)
                LastCliffPosition = MaxIntertidalX
                LastTime = self.Time

                # update plot time
                self.PlotTime += self.PlotInterval

                # update progress bar
                f.value = self.Time

            # update time
            self.Time += self.dt

            # update sea level
            self.SeaLevel += self.SeaLevelRise * self.dt

            # do earthquake?
            if self.Time > self.EarthquakeTime:
                self.Z += self.EarthquakeUplift
                self.EarthquakeTime += self.EarthquakeInterval

        # add colour bar for time to plot
        sm = plt.cm.ScalarMappable(cmap=cm.coolwarm, norm=plt.Normalize(vmin=min(Times), vmax=max(Times)))
        cbar = plt.colorbar(sm, ax=ax1)
        cbar.set_label("Time (years)")

        # finish second plot with cliff retreat rates
        ax2.plot(Times[1:], Rates, 'k--', lw=2)
        ax2.set_xlabel("Time (years)")
        ax2.set_ylabel("Cliff Retreat Rate (m/y)")
        ax2.set_ylim(0, np.max(Rates) * 2)

