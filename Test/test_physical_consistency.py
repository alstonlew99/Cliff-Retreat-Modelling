"""
Test physical consistency of the RockCoast model outputs.

WHY:
  To ensure that cliff retreat and profile changes occur in physically reasonable directions,
  validating the logical behavior of the erosion algorithm.

WHAT:
  - Cliff X positions should not decrease over time
  - Retreat rates (if any) must be non-negative
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "rockcoast"))
import numpy as np
from Model import RockCoast


def test_cliff_retreat_is_monotonic():
    model = RockCoast()
    model.EndTime = 50
    result = model.RunModel(plot=False)

    X = result["X"]
    Rates = result["Rates"]

    assert np.all(np.diff(X) >= -1e-6), "Coastline X positions should not move backward"
    if len(Rates) > 0:
        assert np.all(Rates >= 0), "Retreat rates must be non-negative"
