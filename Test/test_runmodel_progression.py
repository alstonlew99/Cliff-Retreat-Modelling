"""
Test that the RunModel() function advances time and sea level correctly.

WHY:
  The simulation’s core loop should change time and sea level in a predictable way.
  If it doesn’t, the model’s physics are not evolving.

WHAT:
  Run the model for a few iterations (short EndTime) and confirm that:
  - Time increases
  - Sea level rises (or falls) according to SeaLevelRise * actual steps
  - The function returns expected result structure
"""

import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "rockcoast"))
from Model import RockCoast


def test_runmodel_time_and_sealevel_progression():
    model = RockCoast()
    model.EndTime = 10  # shorter run for testing
    model.SeaLevelRise = -0.0035

    # Run model without plotting
    result = model.RunModel(plot=False)

    # --- Basic checks ---
    assert "SeaLevel" in result
    assert np.isclose(result["SeaLevel"], model.SeaLevel), "Returned SeaLevel should match model attribute"
    assert model.Time > 0, "Time should progress during simulation"

    expected_steps = int(model.EndTime / model.dt) + 1
    expected_sealevel = expected_steps * model.SeaLevelRise

    assert np.isclose(model.SeaLevel, expected_sealevel, atol=1e-6), (
        f"Sea level change mismatch: expected {expected_sealevel}, got {model.SeaLevel}"
    )
