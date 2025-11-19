# Cliff-Retreat-Modelling

Cliff Retreat Simulation is a Python-based model for studying the evolution of rocky coasts under the combined effects of wave action, sea-level changes, and tectonic uplift.
The simulation reproduces how coastal profiles evolve over time and how cliff retreat rates respond to environmental parameters.

## Overview
This project includes:

1.A numerical model of cliff retreat (rockcoast/Model.py)

2.A default configuration file for environmental parameters (config.json)

3.An execution script (rockcoast/Run_Cliff_Retreat.py)

4.A complete testing suite (tests/) to ensure model reliability

5.A documentation set (docs/) with tutorials, how-to guides, and theory

## Installation
Clone or download this repository.

**Install dependencies:**

```bash
pip install -r requirements.txt
```
Ensure your environment has Python ≥ 3.9, numpy, matplotlib, and tqdm.

## Running the simulation
The simulation script uses a JSON configuration file to define all environmental and physical parameters.

By default, it loads the configuration file:

config.json


However, you can also provide your own configuration file using the --config (or -c) argument.

### Run using the default configuration
```
python rockcoast/Run_Cliff_Retreat.py
```
### Run using a custom configuration file

If you want to test different environmental scenarios, simply create your own JSON file and pass its path:
```
python rockcoast/Run_Cliff_Retreat.py --config path/to/my_config.json
```

For example:
```
python rockcoast/Run_Cliff_Retreat.py --config configs/high_wave_scenario.json
```

The program will:

Read parameters from JSON file

Initialize the RockCoast model

Simulate coastal profile evolution through time

Save the output plots into the /output folder

Display:

**A time-colored elevation profile**

**A cliff retreat rate vs. time plot**

## Understanding the Output Figures

After the simulation runs, two figures are saved in the `output/` directory.  
These plots summarize how the coastline evolves and how erosion intensity changes through time.

---

### **1. Coastal Profile Evolution (`coastal_profile.png`)**

This figure shows **how the cliff shape evolves over the entire simulation period**.

**Vertical axis:** ground elevation (meters)  
**Horizontal axis:** distance inland from the original shoreline  
**Each colored line:** coastal profile at a specific simulation time  
**Color map:** cool → early years, warm → later years  

**How to interpret the plot:**

If the colored lines move **towards the right**, the coastline is retreating inland.  
Steeper segments represent **more resistant rock**; flatter or shifting areas show **strong erosion**.  
If you see an abrupt upward shift of the entire profile, this corresponds to a **tectonic uplift event**.

This plot provides a visual overview of **long-term coastline shape change** and how waves, sea-level variation, and tectonics interact.

---

### **2. Cliff Retreat Rate (`retreat_rate.png`)**

This plot tracks the **rate at which the cliff retreats** over time.

**Horizontal axis:** simulation time (years)  
**Vertical axis:** retreat rate (meters per year)  
**Dashed line:** change of erosion intensity across time  

**How to interpret the plot:**

High values indicate periods of **strong wave-driven erosion**.  
Lower values correspond to slower retreat, often due to **more resistant material** or **tectonic uplift** reducing wave impact.  
A sudden drop in retreat rate after an uplift event is normal because the cliff is temporarily raised above the active wave zone.

This plot is useful for determining **when erosion is strongest** and for comparing different environmental scenarios across simulations.


## Configuration
Simulation parameters are defined in rockcoast/config.json.
Each parameter controls a physical aspect of the model:

| Parameter                | Description                            | Example |
|--------------------------|----------------------------------------|---------|
| WAVEHEIGHT               | Incoming wave height (m)               | 5       |
| SeaLevelRise             | Annual sea-level change (m/y)          | -0.0035 |
| EarthquakeTime           | Year of tectonic uplift                | 600     |
| EarthquakeUplift         | Vertical displacement (m)              | 5       |
| WaveForceCoef            | Efficiency of wave impact              | 10      |
| DECAY_COEFFICIENT        | Exponential wave energy decay constant | 0.1     |
| TIDAL_RANGE              | Tidal amplitude (m)                    | 2       |
| MAX_RESISTANCE           | Maximum rock strength                  | 2000    |
| MAX_WEATHERING_EFFICIENT | Maximum weathering efficiency          | 100     |

## Documentation
Detailed documentation is available in the /docs folder:

tutorial.md — step-by-step introduction

how_to_guides.md — practical tasks and workflows

reference.md — parameter and API reference

## Author
Yuting Liu
