# Entry point script for running the cliff retreat model.

import argparse
import sys
from rockcoast.config import load_config, ConfigError
from rockcoast.model import CliffRetreatModel

def main():
    parser=argparse.ArgumentParser(description="Run the Cliff Retreat Simulation")
    parser.add_argument(
        "-c", "--config",
        type=str,
        default="examples/example_config.json",
        help="Path to the JSON configuration file (default: examples/example_config.json)"
    )

    args=parser.parse_args()

    try:
        config=load_config(args.config)
    except ConfigError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)

    model=CliffRetreatModel(config)
    model.run()

if __name__ == "__main__":
    main()