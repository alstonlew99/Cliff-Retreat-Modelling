# Tutorial: Run Your First Cliff Retreat Simulation

Welcome!  
In this tutorial, you’ll **build and run your first cliff erosion simulation** using the *Cliff Retreat Simulation* project.  
You’ll start from scratch, configure the model, execute it, visualize the results, and finally modify parameters to see how the cliff’s behavior changes.

By the end, you will have:
- Run a complete simulation without errors  
- Seen how the cliff retreats under wave impact  
- Learned how to adjust environmental parameters  
- Gained the confidence to explore the rest of the project

This tutorial is **hands-on** — you will type commands, edit files, and see immediate results.

---

## Step 1 — Prepare your workspace

First, make sure you have **Python 3.9 or higher** installed.

Then open a terminal (or command prompt) and navigate to your working folder:
```bash
cd Cliff_Retreat_Simulation
```

Check that the folder structure looks like this:
```
Cliff_Retreat_Simulation/
├── rockcoast/
│   ├── Model.py
│   ├── Run_Cliff_Retreat.py
│   └── config.json
└── tests/
```

Now install the dependencies:
```bash
pip install -r requirements.txt
```

## Step 2 — Run the model for the first time

Let’s execute the main script:
```bash
python rockcoast/Run_Cliff_Retreat.py
```

You’ll see a progress bar like:
```
Running Cliff Retreat Simulation:  40%|████    | 400/1000 [00:04<00:06, 90.2it/s]
```

When the simulation finishes, two plots will appear:
1. **Coastal profile evolution** — colored lines show how the cliff face retreats over time.  
2. **Cliff retreat rate** — a dashed line showing retreat velocity (m/y) over simulation years.

If you see both, congratulations — your model is working!

---

## Step 3 — Understand what happened

Let’s interpret what you see.

- **Horizontal axis (Distance)** — how far the cliff front has moved inland.  
- **Vertical axis (Elevation)** — ground height above sea level.  
- **Color gradient** — simulation time, from cool (early) to warm (late).  

The lower plot shows:
- **x-axis:** time in years  
- **y-axis:** rate of retreat in meters per year  

> Every colored profile is one moment in the simulated evolution.  
> The cliff gradually moves landward — that’s erosion in action.

---

## Step 4 — Change the environment

Now we’ll make a meaningful modification.

Open the configuration file:
```
rockcoast/config.json
```

Find these lines:
```json
"SeaLevelRise": -0.0035,
"WAVEHEIGHT": 5
```

Change them to:
```json
"SeaLevelRise": 0.002,
"WAVEHEIGHT": 3
```

Save the file and rerun the simulation:
```bash
python rockcoast/Run_Cliff_Retreat.py
```

Observe the difference:
- The **positive SeaLevelRise** means the sea is rising → erosion is faster.
- The **smaller WAVEHEIGHT** weakens impact → cliff retreats more slowly.

Try changing **only one parameter at a time** and compare how the plots change.

## Step 5 — Run without visualization

Sometimes you just want to test the code or collect numerical results.

In a Python shell or script:
```python
from rockcoast.Model import RockCoast
model = RockCoast()
result = model.RunModel(plot=False)
print(result["SeaLevel"])
```

You’ll see the final sea level value, proving the simulation runs even without plots.  
This is especially useful for automated testing.

---

## Step 6 — Verify that everything still works

To check your environment and the integrity of the project, run:
```bash
pytest -v
```

You should see something like:
```
=================== test session starts ===================
collected 4 items

tests/test_initial_conditions.py ....                      [25%]
tests/test_parameter_assignment.py ....                    [50%]
tests/test_runmodel_progression.py ....                    [75%]
tests/test_physical_consistency.py ....                    [100%]
=================== 4 passed in 5.32s =====================
```

If all tests pass — your setup is correct.

---

## Step 7 — Next exploration ideas

Now that your simulation runs successfully, you can:
- Investigate **tidal range** (`TIDAL_RANGE`) effects  
- Simulate **earthquake uplift** by changing `EarthquakeUplift`  
- Modify `WaveForceCoef` to simulate stronger storms  
- Compare results with different rock resistances (`MAX_RESISTANCE`)  

Every change teaches you something about how coastal processes interact.

---

## Summary

By completing this tutorial, you have:
1. Installed and configured the simulation  
2. Successfully executed a full model run  
3. Visualized coastal retreat over time  
4. Modified environmental parameters  
5. Learned how to test and verify results  

You are now ready to explore the **How-to Guides** and **Reference** sections to perform more advanced experiments.
