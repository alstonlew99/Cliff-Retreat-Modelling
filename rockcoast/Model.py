# import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import rc
from tqdm import tqdm
import os

rc("font", size=16)


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

        # Class properties for caching (initialized in setup_model)
        self.Zw = None
        self.WeatheringEfficacy = None


    # 1. Initial Settings
    def setup_model_state(self):
        """
        Resets the domain, sea level, and pre-calculates tides and weathering distributions.
        Equivalent to the setup block at the start of the original RunModel.
        """
        # reset the initial model domain
        self.Z = np.arange(self.ZMin, self.ZMax, self.dz)
        self.X = self.Z / self.InitialSlope

        # set up an array to collect wave energy in (kept for strict consistency, though unused in loop)
        CumulativeWaveHeight = np.zeros(len(self.Z))

        # create tidal water levels
        TideTime = np.arange(0, 24., 0.1)
        self.Zw = 0.5 * self.TidalRange * np.sin(TideTime * 2. * np.pi / 12.)

        # set up weathering distribution
        IntertidalElevations = np.arange(0.5 * self.TidalRange, -0.5 * self.TidalRange - 0.000001, -self.dz)
        self.WeatheringEfficacy = np.zeros(len(IntertidalElevations))

        # find the location of the maximimum weathering rate
        MaxWeatheringInd = np.argmin(np.abs(IntertidalElevations - 0.25 * self.TidalRange))

        # calculate the distribution of weathering rates
        self.WeatheringEfficacy[0:MaxWeatheringInd] = self.MaxWeatheringEfficacy * np.exp(
            -((IntertidalElevations[0:MaxWeatheringInd] - 0.25 * self.TidalRange) ** 2.) / (
                    0.1 * 0.25 * self.TidalRange))
        self.WeatheringEfficacy[MaxWeatheringInd:] = self.MaxWeatheringEfficacy * np.exp(
            -(0.25 * self.TidalRange - IntertidalElevations[MaxWeatheringInd:]) ** 2. / (0.25 * self.TidalRange))
        self.WeatheringEfficacy = self.WeatheringEfficacy[::-1]


    # 2. Simulation Step (Physics Only)
    def run_simulation_step(self):
        """
        Performs the physical calculations for one time step:
        Waves, Weathering, Erosion, and Collapse.
        Does NOT update Time or Sea Level (handled in RunModel to preserve logic order).

        Returns:
            MaxIntertidalX (float): The position of the cliff for tracking.
        """
        # find high and low tide positions
        LowTideInd = np.argmin(np.abs(self.SeaLevel - 0.5 * self.TidalRange - self.Z))
        HighTideInd = np.argmin(np.abs(self.SeaLevel + 0.5 * self.TidalRange - self.Z))

        # Calculate Total Wave Force impacting the coast over a tidal cycle
        WaveForce = np.zeros(len(self.Z))

        # set up a loop to consider each water level in the progressive position of the tide in turn
        for WaterLevel in self.Zw:

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
            # Safety check for indices to avoid out of bounds if geometry shifts drastically
            if (i - LowTideInd) < len(self.WeatheringEfficacy):
                self.Resistance[i] -= self.WeatheringEfficacy[i - LowTideInd]

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

        return MaxIntertidalX


    # 3. Plotting (Finalizing and Saving)
    def save_final_figures(self, plot, fig1, ax1, fig2, ax2, Times, Rates):
        """
        Handles the final creation of colorbars and saving of figures to the output directory.

        """
        if plot:
            # add colour bar for time to plot
            sm = plt.cm.ScalarMappable(cmap=cm.coolwarm, norm=plt.Normalize(vmin=min(Times), vmax=max(Times)))
            cbar = plt.colorbar(sm, ax=ax1)
            cbar.set_label("Time (years)")

            # finish second plot with cliff retreat rates
            # handle slicing to match original logic (Times[1:])
            if len(Times) > 1 and len(Rates) > 0:
                ax2.plot(Times[1:], Rates, 'k--', lw=2)
                ax2.set_xlabel("Time (years)")
                ax2.set_ylabel("Cliff Retreat Rate (m/y)")
                ax2.set_ylim(0, np.max(Rates) * 2)

            # Save figures to /output folder
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            output_dir = os.path.join(project_root, "output")

            os.makedirs(output_dir, exist_ok=True)

            fig1_path = os.path.join(output_dir, "coastal_profile.png")
            fig2_path = os.path.join(output_dir, "retreat_rate.png")

            fig1.savefig(fig1_path, dpi=300, bbox_inches="tight")
            fig2.savefig(fig2_path, dpi=300, bbox_inches="tight")

            print(f"Saved: {fig1_path}")
            print(f"Saved: {fig2_path}")


    # 4. Simulation (Main Loop)
    def RunModel(self, plot=True):
        """
        Run the coastal retreat simulation.

        """

        progress_bar = tqdm(total=int(self.EndTime - self.Time),
                            desc="Running Cliff Retreat Simulation", ncols=80)

        # set up a figure for plotting the profile results
        fig1, ax1 = None, None
        fig2, ax2 = None, None

        if plot:
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

        # 1. Call Initial Settings
        self.setup_model_state()

        # Initialize tracking variables (local to the run)
        LastCliffPosition = 0
        LastTime = 0

        # loop through time and update hillslope morphology
        while self.Time <= self.EndTime:

            # 2. Call Simulation Step (Physics)
            # returns the MaxIntertidalX calculated in this step
            MaxIntertidalX = self.run_simulation_step()

            # plot the model progress
            # (Logic strictly preserved from original: check time, plot, then update variables)
            if self.Time == 0:
                if plot:
                    ax1.plot(self.X, self.Z, color=cm.coolwarm(self.Time / self.EndTime))
                Times.append(self.PlotTime)
                LastCliffPosition = MaxIntertidalX
                LastTime = self.Time
                self.PlotTime += self.PlotInterval
                progress_bar.update(self.dt)

            elif self.Time >= self.PlotTime:
                if plot:
                    ax1.plot(self.X, self.Z, color=cm.coolwarm(self.Time / self.EndTime))
                Times.append(self.PlotTime)

                Rate = (MaxIntertidalX - LastCliffPosition) / (self.Time - LastTime)
                Rates.append(Rate)
                LastCliffPosition = MaxIntertidalX
                LastTime = self.Time

                self.PlotTime += self.PlotInterval
                progress_bar.update(self.PlotInterval)

            # update time
            self.Time += self.dt

            # update sea level
            self.SeaLevel += self.SeaLevelRise * self.dt

            # do earthquake?
            if self.Time > self.EarthquakeTime:
                self.Z += self.EarthquakeUplift
                self.EarthquakeTime += self.EarthquakeInterval

        progress_bar.close()

        # 3. Call Plotting (Final save)
        # Added fig2 to arguments here
        self.save_final_figures(plot, fig1, ax1, fig2, ax2, Times, Rates)

        return {
            "Times": np.array(Times),
            "Rates": np.array(Rates),
            "X": self.X.copy(),
            "Z": self.Z.copy(),
            "SeaLevel": self.SeaLevel,
        }