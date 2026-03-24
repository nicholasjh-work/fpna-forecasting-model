"""Shared test fixtures for the FP&A forecasting model."""
import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_revenue_df():
    """24 months of synthetic revenue for one division and product."""
    np.random.seed(42)
    months = pd.date_range("2023-01-01", periods=24, freq="MS")
    base_volume = 500
    base_price = 2500.0

    volumes = base_volume + np.random.randint(-50, 80, size=24)
    prices = base_price + np.cumsum(np.random.uniform(-10, 15, size=24))

    return pd.DataFrame({
        "division": "Division A",
        "product_line": "Product 1",
        "month": months,
        "units_sold": volumes,
        "net_revenue": (volumes * prices).round(2),
        "cogs": (volumes * prices * 0.6).round(2),
        "avg_price": prices.round(2),
        "active_customers": np.random.randint(40, 55, size=24),
    })


@pytest.fixture
def sample_features_df(sample_revenue_df):
    """Revenue data with features already generated."""
    from src.feature_engineering import build_features
    return build_features(sample_revenue_df)
