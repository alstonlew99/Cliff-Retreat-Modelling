from matplotlib import pyplot as plt
from Model import RockCoast
import json
import argparse
import os

def main():

    parser = argparse.ArgumentParser(
        description="Run Cliff Retreat Simulation with a given configuration file."
    )

    default_config = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "config.json")
    )

    parser.add_argument(
        "-c", "--config",
        type=str,
        default=default_config,
        help="Path to configuration file (default: project_root/config.json)"
    )

    args = parser.parse_args()
    config_path = os.path.abspath(args.config)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as f:
        config = json.load(f)

    CR = RockCoast()
    CR.SeaLevelRise = config["SeaLevelRise"]
    CR.EarthquakeTime = config["EarthquakeTime"]
    CR.EarthquakeUplift = config["EarthquakeUplift"]
    CR.InitialSlope = config["InitialSlope"]

    CR.WaveHeight = config["WAVEHEIGHT"]
    CR.WaveForceCoef = config["WaveForceCoef"]
    CR.WaveDecayCoef = config["DECAY_COEFFICIENT"]
    CR.TidalRange = config["TIDAL_RANGE"]

    CR.MaxResistance = config["MAX_RESISTANCE"]
    CR.MaxWeatheringEfficacy = config["MAX_WEATHERING_EFFICIENT"]

    CR.RunModel()
    plt.show()

if __name__ == "__main__":
    main()
