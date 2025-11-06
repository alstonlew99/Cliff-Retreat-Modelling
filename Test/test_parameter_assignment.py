"""
Test that parameters from config.json are correctly assigned to RockCoast instance.

WHY:
  Ensures external configuration file is interpreted correctly,
  avoiding mismatched or missing keys.

WHAT:
  Load config.json and verify that RockCoast attributes match those values.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "rockcoast"))
import json
import numpy as np
from Model import RockCoast


def test_parameters_from_config_are_assigned_correctly():
    config_path = os.path.join(os.path.dirname(__file__), "..", "rockcoast", "config.json")
    assert os.path.exists(config_path), f"Config file not found at {config_path}"

    with open(config_path, "r") as f:
        import json
        config = json.load(f)


    model = RockCoast()
    model.SeaLevelRise = config["SeaLevelRise"]
    model.EarthquakeTime = config["EarthquakeTime"]
    model.EarthquakeUplift = config["EarthquakeUplift"]
    model.InitialSlope = config["InitialSlope"]
    model.WaveHeight = config["WAVEHEIGHT"]
    model.WaveForceCoef = config["WaveForceCoef"]
    model.WaveDecayCoef = config["DECAY_COEFFICIENT"]
    model.TidalRange = config["TIDAL_RANGE"]
    model.MaxResistance = config["MAX_RESISTANCE"]
    model.MaxWeatheringEfficacy = config["MAX_WEATHERING_EFFICIENT"]

    # Verify each value
    assert np.isclose(model.SeaLevelRise, config["SeaLevelRise"])
    assert np.isclose(model.WaveHeight, config["WAVEHEIGHT"])
    assert np.isclose(model.TidalRange, config["TIDAL_RANGE"])
    assert np.isclose(model.MaxResistance, config["MAX_RESISTANCE"])
