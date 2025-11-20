import unittest
import numpy as np
import sys
import os

# Add the parent directory to sys.path to locate the 'rockcoast' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import from the rockcoast package
from rockcoast.Model import RockCoast


class TestRockCoastInitialization(unittest.TestCase):

    def setUp(self):
        """Create a fresh instance before each test."""
        self.model = RockCoast()

    def test_defaults(self):
        """Test if default parameters are set correctly in __init__."""
        self.assertEqual(self.model.Time, 0)
        self.assertEqual(self.model.InitialSlope, 1.0)
        self.assertIsNone(self.model.Zw, "Zw should be None before setup_model_state is called")

    def test_setup_model_state(self):
        """Test if setup_model_state initializes arrays correctly."""
        self.model.setup_model_state()

        # Check spatial domains
        self.assertTrue(len(self.model.Z) > 0, "Z array should not be empty")
        self.assertEqual(len(self.model.Z), len(self.model.X), "Z and X should have the same length")

        # Check Tide Generation (Zw)
        # TideTime was np.arange(0, 24, 0.1) -> 240 elements
        expected_tide_len = len(np.arange(0, 24., 0.1))
        self.assertIsNotNone(self.model.Zw, "Zw should be initialized")
        self.assertEqual(len(self.model.Zw), expected_tide_len, "Tidal array Zw has incorrect length")

        # Check Weathering Efficacy
        self.assertIsNotNone(self.model.WeatheringEfficacy, "WeatheringEfficacy should be initialized")
        # It should contain positive values where weathering occurs
        self.assertTrue(np.max(self.model.WeatheringEfficacy) > 0, "Max weathering efficacy should be positive")


if __name__ == '__main__':
    print("Running Initialization Tests...")
    unittest.main()