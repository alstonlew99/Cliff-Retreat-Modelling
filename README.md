# Cliff-Retreat-Modelling

Cliff Retreat Simulation is a Python-based model for studying the evolution of rocky coasts under the combined effects of wave action, sea-level changes, and tectonic uplift.
The simulation reproduces how coastal profiles evolve over time and how cliff retreat rates respond to environmental parameters.

## Overview
This project includes:

1.A numerical model of cliff retreat (rockcoast/Model.py)

2.A configuration file for environmental parameters (rockcoast/config.json)

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
From the project root:
```
python rockcoast/Run_Cliff_Retreat.py
```

The program will:

Read parameters from *config.json*

Initialize the RockCoast model

Simulate coastal profile evolution through time

Display:

**A time-colored elevation profile**

**A cliff retreat rate vs. time plot**

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

explanation.md — physical model and numerical rationale

reference.md — parameter and API reference

## Author
Yuting Liu
