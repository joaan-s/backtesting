import json
from src.backtester import Backtester, DeathCrossStrategy

CONFIG_PATH = "config.json"


def load_config(path=CONFIG_PATH):
    """Load settings from the config file."""
    with open(path) as f:
        return json.load(f)


def build_strategy(config):
    """Build the strategy object based on the 'strategy' field in config."""
    strategy_name = config.get("strategy")

    if strategy_name == "death_cross":
        params = config["death_cross"]
        return DeathCrossStrategy(
            short_window=params["short_window"],
            long_window=params["long_window"]
        )

    raise ValueError(f"Unknown strategy '{strategy_name}' in {CONFIG_PATH}")


if __name__ == "__main__":
    config = load_config()

    # Create a backtester using values from the config file
    backtester = Backtester(config["ticker"], config["start_date"], config["end_date"])

    # Download the data
    backtester.download_data()

    # Build the strategy from config (parameters like short_window/long_window
    # can be tweaked in config.json without touching this file)
    strategy = build_strategy(config)

    # Run trading strategy
    backtester.run_batch_test(strategy)
