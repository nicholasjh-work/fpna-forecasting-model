"""
Linear regression model for revenue forecasting.

Trains on driver-based features, evaluates with MAPE, WAPE, and bias.
Cross-validates with 5-fold time-series split.

Usage:
    python -m src.model
"""
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
MODEL_DIR = Path(__file__).parent.parent / "models"

FEATURE_COLS = [
    "volume_lag_1", "volume_lag_3", "volume_rolling_3m", "volume_rolling_12m",
    "price_index", "price_change_pct", "mix_share",
    "month_sin", "month_cos", "is_q4", "volume_yoy_pct",
]

TARGET_COL = "net_revenue"


def train_evaluate(df: pd.DataFrame) -> dict:
    """Train the model and return evaluation metrics."""
    df = df.sort_values("month").reset_index(drop=True)

    X = df[FEATURE_COLS].values
    y = df[TARGET_COL].values

    # Train/test split: last 20% for testing (time-ordered, no shuffle)
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # Train
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Metrics
    mape = mean_absolute_percentage_error(y_test, y_pred) * 100
    mae = mean_absolute_error(y_test, y_pred)
    wape = np.sum(np.abs(y_test - y_pred)) / np.sum(np.abs(y_test)) * 100
    bias = np.mean(y_pred - y_test) / np.mean(y_test) * 100

    # Baseline: last-value holdout (predict = previous month actual)
    y_baseline = y[split_idx - 1 : len(y) - 1]
    if len(y_baseline) == len(y_test):
        baseline_mape = mean_absolute_percentage_error(y_test, y_baseline) * 100
    else:
        baseline_mape = float("nan")

    # Feature importance (coefficients, normalized)
    coef_abs = np.abs(model.coef_)
    coef_norm = coef_abs / coef_abs.sum()
    importance = sorted(
        zip(FEATURE_COLS, model.coef_, coef_norm),
        key=lambda x: abs(x[1]),
        reverse=True,
    )

    # Cross-validation
    tscv = TimeSeriesSplit(n_splits=5)
    cv_mapes = []
    for train_idx, val_idx in tscv.split(X):
        m = LinearRegression()
        m.fit(X[train_idx], y[train_idx])
        pred = m.predict(X[val_idx])
        cv_mape = mean_absolute_percentage_error(y[val_idx], pred) * 100
        cv_mapes.append(cv_mape)

    results = {
        "mape": round(mape, 2),
        "wape": round(wape, 2),
        "mae": round(mae, 2),
        "bias_pct": round(bias, 2),
        "baseline_mape": round(baseline_mape, 2),
        "cv_mapes": [round(m, 2) for m in cv_mapes],
        "cv_mape_mean": round(np.mean(cv_mapes), 2),
        "cv_mape_std": round(np.std(cv_mapes), 2),
        "feature_importance": [
            {"feature": f, "coefficient": round(c, 4), "importance": round(i, 4)}
            for f, c, i in importance
        ],
        "train_size": len(X_train),
        "test_size": len(X_test),
    }

    return results, model


def main():
    features_path = DATA_DIR / "features.csv"
    if not features_path.exists():
        logger.error("No features file found. Run feature_engineering first.")
        return

    df = pd.read_csv(features_path, parse_dates=["month"])
    logger.info("Loaded %d rows with %d features", len(df), len(FEATURE_COLS))

    results, model = train_evaluate(df)

    logger.info("Model evaluation:")
    logger.info("  MAPE: %.2f%% (baseline: %.2f%%)", results["mape"], results["baseline_mape"])
    logger.info("  WAPE: %.2f%%", results["wape"])
    logger.info("  Bias: %+.2f%%", results["bias_pct"])
    logger.info("  CV MAPE: %.2f%% +/- %.2f%%", results["cv_mape_mean"], results["cv_mape_std"])
    logger.info("  Top features:")
    for fi in results["feature_importance"][:5]:
        logger.info("    %s: coef=%.4f, importance=%.1f%%", fi["feature"], fi["coefficient"], fi["importance"] * 100)

    # Save model coefficients (not pickle, for auditability)
    MODEL_DIR.mkdir(exist_ok=True)
    coef_df = pd.DataFrame(results["feature_importance"])
    coef_df.to_csv(MODEL_DIR / "coefficients.csv", index=False)
    logger.info("Saved coefficients to models/coefficients.csv")


if __name__ == "__main__":
    main()
