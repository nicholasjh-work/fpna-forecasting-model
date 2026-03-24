"""
Scenario and sensitivity analysis.

Takes a base forecast and applies volume, price, and mix shocks
to generate alternative revenue projections.

Usage:
    python -m src.scenario --scenario conservative
    python -m src.scenario --volume 0.9 --price 1.05
"""
import argparse
import logging
from pathlib import Path

import pandas as pd
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
CONFIG_DIR = Path(__file__).parent.parent / "config"


def load_scenarios() -> dict:
    path = CONFIG_DIR / "scenarios.yaml"
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f).get("scenarios", {})
    return {
        "base": {"volume_factor": 1.0, "price_factor": 1.0},
        "conservative": {"volume_factor": 0.92, "price_factor": 0.98},
        "optimistic": {"volume_factor": 1.08, "price_factor": 1.03},
    }


def apply_scenario(
    forecast_df: pd.DataFrame,
    volume_factor: float = 1.0,
    price_factor: float = 1.0,
    label: str = "custom",
) -> pd.DataFrame:
    """Apply volume and price shocks to a forecast."""
    result = forecast_df.copy()
    combined_factor = volume_factor * price_factor
    result["forecast_revenue"] = (result["forecast_revenue"] * combined_factor).round(2)
    result["lower_bound_95"] = (result["lower_bound_95"] * combined_factor).round(2)
    result["upper_bound_95"] = (result["upper_bound_95"] * combined_factor).round(2)
    result["scenario"] = label
    result["volume_factor"] = volume_factor
    result["price_factor"] = price_factor
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", default=None, help="Named scenario from config")
    parser.add_argument("--volume", type=float, default=None, help="Volume factor (0.9 = 10%% drop)")
    parser.add_argument("--price", type=float, default=None, help="Price factor (1.05 = 5%% increase)")
    args = parser.parse_args()

    forecast_path = DATA_DIR / "forecast_output.csv"
    if not forecast_path.exists():
        logger.error("No forecast output. Run forecast first.")
        return

    forecast_df = pd.read_csv(forecast_path, parse_dates=["month"])

    if args.scenario:
        scenarios = load_scenarios()
        if args.scenario not in scenarios:
            logger.error("Unknown scenario '%s'. Available: %s", args.scenario, list(scenarios.keys()))
            return
        s = scenarios[args.scenario]
        result = apply_scenario(forecast_df, s["volume_factor"], s["price_factor"], args.scenario)
    elif args.volume or args.price:
        result = apply_scenario(
            forecast_df,
            args.volume or 1.0,
            args.price or 1.0,
            "custom",
        )
    else:
        # Run all named scenarios
        scenarios = load_scenarios()
        results = []
        for name, s in scenarios.items():
            r = apply_scenario(forecast_df, s["volume_factor"], s["price_factor"], name)
            results.append(r)
        result = pd.concat(results, ignore_index=True)

    output_path = DATA_DIR / "scenario_output.csv"
    result.to_csv(output_path, index=False)
    logger.info("Scenario output saved to %s (%d rows)", output_path, len(result))

    for _, row in result.iterrows():
        logger.info(
            "  [%s] %s: $%s (vol=%.2f, price=%.2f)",
            row["scenario"],
            row["month"].strftime("%Y-%m") if hasattr(row["month"], "strftime") else row["month"],
            f"{row['forecast_revenue']:,.0f}",
            row["volume_factor"],
            row["price_factor"],
        )


if __name__ == "__main__":
    main()
