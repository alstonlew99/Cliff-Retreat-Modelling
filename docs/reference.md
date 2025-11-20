# Reference Guide: Cliff Retreat Simulation Codebase

This reference guide provides a **technical description** of the key components in the *Cliff Retreat Simulation* project.
It lists the public classes, functions, attributes, and configuration parameters used by the model.

This section is **information-oriented** — it tells you what exists and how to use it, but does not explain theory or workflows.  
For conceptual or instructional material, see the *Tutorials* and *How-to Guides* sections.

---

## Module: `rockcoast.Model`

### Class: `RockCoast`

Main class representing the coastal system.  
Encapsulates physical parameters, state variables, and the simulation loop.

#### Initialization

```python
model = RockCoast()
```
Creates a new model instance with default settings.

#### Attributes

| Attribute             | Type    | Description                               | Default  |
|-----------------------|---------|-------------------------------------------|----------|
| InitialSlope          | float   | Initial slope of the coastal profile      | 1.0      |
| dz                    | float   | Spatial discretization step (m)           | 0.1      |
| ZMax / ZMin           | float   | Maximum and minimum elevations (m)        | 10 / -10 |
| Z, X                  | ndarray | Vertical and horizontal coordinate arrays | computed |
| WaveHeight            | float   | Incident wave height (m)                  | 2.0      |
| WaveForceCoef         | float   | Efficiency coefficient for wave energy    | 10       |
| WaveDecayCoef         | float   | Exponential decay rate of wave energy     | 0.1      |
| TidalRange            | float   | Total tidal amplitude (m)                 | 2.0      |
| SeaLevel              | float   | Current sea level (m)                     | 0.0      |
| SeaLevelRise          | float   | Rate of sea-level change (m/year)         | 0.0      |
| EarthquakeUplift      | float   | Vertical uplift during seismic event (m)  | 0.0      |
| EarthquakeTime        | float   | Time (years) when earthquake occurs       | 1000     |
| EarthquakeInterval    | float   | Period between uplift events (y)          | 1000     |
| MaxResistance         | float   | Maximum rock resistance                   | 2000     |
| Resistance            | ndarray | Resistance profile across cliff           | uniform  |
| MaxWeatheringEfficacy | float   | Maximum intertidal weathering rate        | 100      |
| Time                  | float   | Current simulation time (y)               | 0        |
| dt                    | float   | Time step (y)                             | 1        |
| EndTime               | float   | Simulation duration (y)                   | 1000     |
| PlotFigures           | bool    | Whether to show plots                     | True     |
| PlotTime              | float   | Next scheduled plot time (y)              | 0        |
| PlotInterval          | float   | Time interval between plots (y)           | 100      |

---

#### Method: `RunModel(plot=True)`

Runs the time-evolution of the cliff profile.

### Class: `RockCoast`

Main class representing the coastal system.  
Encapsulates physical parameters, state variables, and the simulation loop.

##### Signature
```python
result = model.RunModel(plot=True)
```

##### Parameters
| Parameter | Type | Description                                                                                                  |
|-----------|------|--------------------------------------------------------------------------------------------------------------|
| plot      | bool | If True, generate plots of cliff profile and retreat rate. If False, run headless (for tests or automation). |

##### Returns
A dictionary containing simulation outputs:
```python
{
    "Times": np.ndarray,   # time points used for plotting
    "Rates": np.ndarray,   # cliff retreat rates (m/y)
    "X": np.ndarray,       # horizontal coordinates
    "Z": np.ndarray,       # vertical coordinates
    "SeaLevel": float      # final sea level
}
```

##### Behaviour
- Initializes model domain (`Z`, `X` arrays).  
- Iterates through time until `Time > EndTime`.  
- Updates sea level, wave energy, and rock resistance each iteration.  
- Applies erosion if wave force exceeds resistance.  
- Plots results if `plot=True` using `matplotlib`.  
- Returns arrays for further analysis when complete.

##### Precautions
- Ensure parameters (especially `dz` and `dt`) are small enough for numerical stability.  
- If modifying arrays within the loop, preserve dimensional consistency between `Z`, `X`, and `Resistance`.  
- When extending the class, always call `super().__init__()` in derived versions.

---

## Module: `rockcoast.Run_Cliff_Retreat`

Entry script to execute the model with parameters read from `config.json`.

### Execution

```bash
python rockcoast/Run_Cliff_Retreat.py
```

### Description
1. Loads configuration parameters via Python’s `json` module.  
2. Instantiates `RockCoast`.  
3. Assigns parameters from the config file.  
4. Calls `RunModel()`.  
5. Displays resulting plots.

---

## Configuration File: `rockcoast/config.json`

Defines physical and environmental parameters used in the simulation.  
Values are read as floats or integers and assigned to corresponding `RockCoast` attributes.

| Key                      | Maps to Attribute     | Description                           | Example |
|--------------------------|-----------------------|---------------------------------------|---------|
| WAVEHEIGHT               | WaveHeight            | Incoming wave height (m)              | 5       |
| SLOPE                    | InitialSlope          | Initial slope ratio                   | 0.02    |
| DECAY_COEFFICIENT        | WaveDecayCoef         | Wave energy decay constant            | 0.1     |
| TIDAL_RANGE              | TidalRange            | Tidal range (m)                       | 2       |
| SeaLevelRise             | SeaLevelRise          | Annual change in sea level (m/y)      | -0.0035 |
| EarthquakeTime           | EarthquakeTime        | Time of uplift (years)                | 600     |
| EarthquakeUplift         | EarthquakeUplift      | Vertical uplift during event (m)      | 5       |
| WaveForceCoef            | WaveForceCoef         | Efficiency coefficient of wave energy | 10      |
| MAX_RESISTANCE           | MaxResistance         | Maximum rock resistance               | 2000    |
| MAX_WEATHERING_EFFICIENT | MaxWeatheringEfficacy | Maximum weathering rate               | 100     |

---

## Module: `tests/`

Contains automated tests verifying model integrity.

| File                         | Purpose                                                          |
|------------------------------|------------------------------------------------------------------|
| test_initial_conditions.py   | Checks initialization defaults of RockCoast                      |
| test_parameter_assignment.py | Confirms configuration values are correctly assigned             |
| test_runmodel_progression.py | Ensures time and sea-level evolution follow expected progression |
| test_physical_consistency.py | Validates erosion direction and non-negative retreat rates       |

Each test uses **pytest** and **NumPy**’s `isclose()` for floating-point safety.

---

## Dependencies

| Library    | Purpose                                      |
|------------|----------------------------------------------|
| numpy      | Numerical computation and arrays             |
| matplotlib | Plotting elevation and retreat rate profiles |
| tqdm       | Progress bar during simulation               |
| pytest     | Automated testing framework                  |
| json       | Configuration parsing                        |

---

## Usage Example

```python
from rockcoast.Model import RockCoast

model = RockCoast()
model.SeaLevelRise = -0.0035
model.WaveHeight = 5
results = model.RunModel(plot=False)

print(results["SeaLevel"])
```
Outputs the final sea level after the simulation completes.

---

## Notes

- All physical constants are expressed in SI units.  
- The simulation is deterministic — repeated runs with identical parameters will yield identical outputs.  
- Visualization functions are not tested by default.  
- Extending the code requires basic familiarity with Python OOP and numerical modeling.
