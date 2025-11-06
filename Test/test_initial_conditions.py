"""
Test that the RockCoast model initializes with correct default parameters.

WHY:
  The initialization defines the starting state of the model. If defaults are wrong,
  every simulation outcome will be invalid.

WHAT:
  This test checks that the initial parameters and arrays match the expected defaults.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "rockcoast"))
import numpy as np
from Model import RockCoast


def test_initial_conditions_are_correct():
    model = RockCoast()
    assert np.isclose(model.InitialSlope, 1.0), "Initial slope should be 1.0"
    assert np.isclose(model.WaveHeight, 2.0), "Default wave height should be 2 m"
    assert np.isclose(model.SeaLevel, 0.0), "Sea level should start at 0"
    assert np.allclose(model.Resistance, model.MaxResistance), "Initial resistance should be uniform"
    assert model.Z.shape == model.X.shape, "Z and X arrays must have same shape"
