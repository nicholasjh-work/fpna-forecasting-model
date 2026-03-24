"""
Export forecast KPIs to CSV for Tableau consumption.

Merges actuals with forecasts and scenario outputs into a single
file that Tableau can import as a data source.

Usage:
    python -m src.export
"""
import logging
from pathlib import Path

import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"


def main():
    features_path = DATA_DIR / "features.csv"
    forecast_path = DATA_DIR / "forecast_output.csv"

    if not features_path.exists():
        logger.error("No features file found.")
        return

    actuals = pd.read_csv(features_path, parse_dates=["month"])
    actuals = actuals[["division", "product_line", "month", "net_revenue", "units_sold", "avg_price"]].copy()
    actuals["record_type"] = "actual"
    actuals["scenario"] = "actual"

    if forecast_path.exists():
        forecast = pd.read_csv(forecast_path, parse_dates=["month"])
        forecast["record_type"] = "forecast"
        forecast["scenario"] = forecast.get("scenario", "base")
        forecast = forecast.rename(columns={"forecast_revenue": "net_revenue"})
    else:
        forecast = pd.DataFrame()

    # Scenario output
    scenario_path = DATA_DIR / "scenario_output.csv"
    if scenario_path.exists():
        scenarios = pd.read_csv(scenario_path, parse_dates=["month"])
        scenarios["record_type"] = "scenario"
        scenarios = scenarios.rename(columns={"forecast_revenue": "net_revenue"})
    else:
        scenarios = pd.DataFrame()

    combined = pd.concat([actuals, forecast, scenarios], ignore_index=True)

    output_path = DATA_DIR / "tableau_export.csv"
    combined.to_csv(output_path, index=False)
    logger.info("Exported %d rows to %s", len(combined), output_path)
    logger.info("  Actuals: %d rows", len(actuals))
    logger.info("  Forecast: %d rows", len(forecast))
    logger.info("  Scenarios: %d rows", len(scenarios))


if __name__ == "__main__":
    main()
