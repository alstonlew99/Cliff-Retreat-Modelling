# How-to Guides: Practical Recipes for Cliff Retreat Simulation

These guides answer specific questions about using or modifying the **Cliff Retreat Simulation** project.
They assume you already know how to run the simulation once and now want to achieve a concrete goal.

Each section starts with a question like “How do I…?” and provides the minimum necessary steps to reach that goal.

---

## How to change the simulation duration

**Goal:** Run a shorter (or longer) simulation to test new parameters quickly.

### Steps

1. Open the file `rockcoast/Model.py`.
2. Find the following line near the top of the `__init__` method:
   ```python
   self.EndTime = 1000.  # time the model will stop (y)
   ```
3. Change `1000.` to a new value (e.g., `100.` for faster runs or `5000.` for long-term evolution).
4. Save the file.
5. Run:
   ```bash
   python rockcoast/Run_Cliff_Retreat.py
   ```
6. Observe that the simulation completes more quickly (or more slowly).

---

## How to adjust wave force and decay

**Goal:** Modify wave energy intensity or attenuation.

### Steps

1. Open `rockcoast/config.json`.
2. Locate the following parameters:
   ```json
   "WaveForceCoef": 10,
   "DECAY_COEFFICIENT": 0.1
   ```
3. Increase `WaveForceCoef` to simulate more energetic waves (e.g., `20`).
4. Increase `DECAY_COEFFICIENT` to make energy decay faster toward the shore (e.g., `0.2`).
5. Save and re-run the simulation.
6. Compare retreat rates before and after — stronger waves should erode faster, higher decay should localize erosion closer to shore.

---

## How to modify rock resistance or weathering

**Goal:** Represent different rock materials (e.g., hard basalt vs. soft sandstone).

### Steps

1. Open `rockcoast/config.json`.
2. Change these parameters:
   ```json
   "MAX_RESISTANCE": 2000,
   "MAX_WEATHERING_EFFICIENT": 100
   ```
3. Lower `MAX_RESISTANCE` (e.g., to `500`) to simulate weak rock.
4. Raise `MAX_WEATHERING_EFFICIENT` (e.g., to `200`) to accelerate weathering.
5. Run the simulation and compare the cliff retreat speed.

---

## How to simulate an earthquake uplift event

**Goal:** Add a tectonic event that lifts the coastline during the simulation.

### Steps

1. Open `rockcoast/config.json`.
2. Find and adjust:
   ```json
   "EarthquakeTime": 600,
   "EarthquakeUplift": 5
   ```
3. Increase `EarthquakeUplift` to raise the terrain more (e.g., `10`).  
4. Change `EarthquakeTime` to make it occur earlier or later (e.g., `200` years).
5. Run the simulation.
6. Notice that after the specified time, the coastline shifts upward — erosion slows temporarily as waves reach a lower level.

---

## How to export results automatically

**Goal:** Save computed arrays (e.g., retreat rates) to a CSV file.

### Steps

1. In `Model.py`, find the end of the `RunModel()` function.
2. Before the `return` statement, insert:
   ```python
   import pandas as pd
   pd.DataFrame({
       "Times": Times,
       "Rates": Rates,
       "X": self.X,
       "Z": self.Z
   }).to_csv("cliff_Retreat_results.csv", index=False)
   ```
3. Run the simulation as usual.
4. Check that `output_results.csv` appears in the working directory.
5. Open it in Excel or a plotting tool to analyze the time–rate relationship.

---

## Summary

These how-to guides provide quick, goal-oriented recipes for the most common tasks:

- Change simulation duration  
- Adjust wave energy and decay  
- Modify rock and weathering properties  
- Simulate earthquake uplift
- Export simulation results

They are designed to be adaptable — feel free to adjust parameters and extend steps to fit your research needs.
