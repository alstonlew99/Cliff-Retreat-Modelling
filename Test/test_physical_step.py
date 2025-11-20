import unittest
import numpy as np
import sys
import os

# Add the parent directory to sys.path to locate the 'rockcoast' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rockcoast.Model import RockCoast


class TestRockCoastPhysics(unittest.TestCase):

    def setUp(self):
        self.model = RockCoast()
        self.model.setup_model_state()

    def test_weathering_decreases_resistance(self):
        """Test if resistance decreases in the intertidal zone after a step."""
        # 1. Disable waves to prevent erosion from resetting the resistance
        #    (We want to isolate the weathering effect)
        self.model.WaveHeight = 0.0

        # 2. Increase weathering efficacy to ensure the change is significant
        self.model.MaxWeatheringEfficacy = 100.0
        # Re-calculate weathering profile with new efficacy
        self.model.setup_model_state()

        # Copy initial resistance
        initial_resistance = self.model.Resistance.copy()

        # Run one step
        self.model.run_simulation_step()

        # Check if resistance has changed anywhere
        has_changed = not np.array_equal(initial_resistance, self.model.Resistance)
        self.assertTrue(has_changed,
                        "Resistance should decrease due to weathering (WaveHeight set to 0 to prevent reset)")

        # Ensure it hasn't increased
        self.assertTrue(np.all(self.model.Resistance <= initial_resistance),
                        "Resistance should not increase during weathering")

    def test_erosion_changes_morphology(self):
        """Test if high wave force causes the cliff (X) to retreat."""
        # Crank up the wave force to guarantee erosion
        self.model.WaveForceCoef = 10000.0
        self.model.WaveHeight = 10.0

        initial_x = self.model.X.copy()

        # Run one step
        current_cliff_pos = self.model.run_simulation_step()

        # Check if X has increased (retreat means X gets larger/moves landward)
        self.assertGreater(np.sum(self.model.X), np.sum(initial_x),
                           "The cliff should retreat (X increases) under high wave force")

        # Check return value
        self.assertIsInstance(current_cliff_pos, float,
                              "run_simulation_step should return a float representing cliff position")


if __name__ == '__main__':
    print("Running Physics Step Tests...")
    unittest.main()