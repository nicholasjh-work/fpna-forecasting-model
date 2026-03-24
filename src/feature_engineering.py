"""
Feature engineering for the FP&A forecasting model.

Generates driver-based features from raw revenue data:
lag values, rolling averages, seasonality encodings, price indices.

All features use only past data. No future leakage.

Usage:
    python -m src.feature_engineering
"""
import logging
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Generate features from raw revenue data.

    Input columns: division, product_line, month, units_sold, net_revenue,
                   avg_price, active_customers
    Output: same columns plus engineered features, NaN rows from lag dropped.
    """
    df = df.copy()
    df["month"] = pd.to_datetime(df["month"])
    df = df.sort_values(["division", "product_line", "month"]).reset_index(drop=True)

    group_cols = ["division", "product_line"]

    # Volume lags
    for lag in [1, 3, 6, 12]:
        df[f"volume_lag_{lag}"] = df.groupby(group_cols)["units_sold"].shift(lag)

    # Volume rolling averages
    for window in [3, 6, 12]:
        df[f"volume_rolling_{window}m"] = (
            df.groupby(group_cols)["units_sold"]
            .transform(lambda x: x.rolling(window, min_periods=window).mean())
        )

    # Year-over-year volume change
    df["volume_yoy_change"] = (
        df["units_sold"] - df.groupby(group_cols)["units_sold"].shift(12)
    )
    df["volume_yoy_pct"] = np.where(
        df.groupby(group_cols)["units_sold"].shift(12) == 0,
        0,
        df["volume_yoy_change"] / df.groupby(group_cols)["units_sold"].shift(12),
    )

    # Price features
    df["price_lag_1"] = df.groupby(group_cols)["avg_price"].shift(1)
    df["price_change_pct"] = np.where(
        df["price_lag_1"] == 0,
        0,
        (df["avg_price"] - df["price_lag_1"]) / df["price_lag_1"],
    )

    # Price index: current price relative to 12-month average
    df["price_rolling_12m"] = (
        df.groupby(group_cols)["avg_price"]
        .transform(lambda x: x.rolling(12, min_periods=12).mean())
    )
    df["price_index"] = np.where(
        df["price_rolling_12m"] == 0,
        1.0,
        df["avg_price"] / df["price_rolling_12m"],
    )

    # Product mix share: product revenue as % of total division revenue that month
    div_monthly_rev = df.groupby(["division", "month"])["net_revenue"].transform("sum")
    df["mix_share"] = np.where(
        div_monthly_rev == 0,
        0,
        df["net_revenue"] / div_monthly_rev,
    )

    # Seasonality encoding (cyclical, avoids discontinuity at Dec/Jan boundary)
    month_num = df["month"].dt.month
    df["month_sin"] = np.sin(2 * np.pi * month_num / 12)
    df["month_cos"] = np.cos(2 * np.pi * month_num / 12)

    # Fiscal year-end flag (Q4 = Apr-Jun for July fiscal year)
    df["is_q4"] = (month_num.isin([4, 5, 6])).astype(int)

    # Customer count lag
    df["customers_lag_1"] = df.groupby(group_cols)["active_customers"].shift(1)

    # Drop rows where lag features are NaN (first 12 months of history)
    feature_cols = [c for c in df.columns if "lag_" in c or "rolling_" in c]
    initial_rows = len(df)
    df = df.dropna(subset=feature_cols).reset_index(drop=True)
    logger.info("Dropped %d rows with NaN lag features (%d remaining)", initial_rows - len(df), len(df))

    return df


def main():
    input_path = DATA_DIR / "revenue_history.csv"
    if not input_path.exists():
        # Fall back to sample data
        input_path = DATA_DIR / "sample" / "sample_revenue.csv"
    if not input_path.exists():
        logger.error("No input data found. Run data_pull first.")
        return

    df = pd.read_csv(input_path, parse_dates=["month"])
    logger.info("Loaded %d rows from %s", len(df), input_path)

    df_features = build_features(df)
    logger.info("Generated %d features, %d rows", len([c for c in df_features.columns if c not in df.columns]), len(df_features))

    output_path = DATA_DIR / "features.csv"
    df_features.to_csv(output_path, index=False)
    logger.info("Saved features to %s", output_path)


if __name__ == "__main__":
    main()
