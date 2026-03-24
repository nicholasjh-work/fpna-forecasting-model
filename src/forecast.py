"""
Generate revenue forecasts with confidence intervals.

Loads the trained model coefficients, applies to the latest feature values,
and produces point forecasts plus 95% confidence bounds.

Usage:
    python -m src.forecast
    python -m src.forecast --periods 6
"""
import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from src.model import FEATURE_COLS, TARGET_COL

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"


def generate_forecast(df: pd.DataFrame, periods: int = 6) -> pd.DataFrame:
    """Train on full history and forecast forward."""
    df = df.sort_values("month").reset_index(drop=True)

    X = df[FEATURE_COLS].values
    y = df[TARGET_COL].values

    model = LinearRegression()
    model.fit(X, y)

    # Residual standard deviation for confidence intervals
    y_pred_train = model.predict(X)
    residual_std = np.std(y - y_pred_train)

    # For forward forecast, use the last available feature row
    # In production, this would use updated lag features for each future month
    last_features = X[-1:].copy()
    forecasts = []

    for i in range(1, periods + 1):
        point = model.predict(last_features)[0]
        lower = point - 1.96 * residual_std
        upper = point + 1.96 * residual_std

        last_month = df["month"].max()
        forecast_month = last_month + pd.DateOffset(months=i)

        forecasts.append({
            "month": forecast_month,
            "forecast_revenue": round(point, 2),
            "lower_bound_95": round(max(0, lower), 2),
            "upper_bound_95": round(upper, 2),
            "residual_std": round(residual_std, 2),
        })

    return pd.DataFrame(forecasts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--periods", type=int, default=6, help="Months to forecast ahead")
    args = parser.parse_args()

    features_path = DATA_DIR / "features.csv"
    if not features_path.exists():
        logger.error("No features file. Run feature_engineering first.")
        return

    df = pd.read_csv(features_path, parse_dates=["month"])
    logger.info("Loaded %d rows", len(df))

    forecast_df = generate_forecast(df, periods=args.periods)

    output_path = DATA_DIR / "forecast_output.csv"
    forecast_df.to_csv(output_path, index=False)
    logger.info("Forecast saved to %s", output_path)

    for _, row in forecast_df.iterrows():
        logger.info(
            "  %s: $%s [%s, %s]",
            row["month"].strftime("%Y-%m"),
            f"{row['forecast_revenue']:,.0f}",
            f"{row['lower_bound_95']:,.0f}",
            f"{row['upper_bound_95']:,.0f}",
        )


if __name__ == "__main__":
    main()
