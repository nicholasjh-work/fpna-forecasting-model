"""Tests for feature engineering."""
import pytest
import numpy as np
import pandas as pd

from src.feature_engineering import build_features


class TestBuildFeatures:
    def test_output_has_lag_columns(self, sample_revenue_df):
        result = build_features(sample_revenue_df)
        assert "volume_lag_1" in result.columns
        assert "volume_lag_3" in result.columns
        assert "volume_lag_12" in result.columns

    def test_output_has_rolling_columns(self, sample_revenue_df):
        result = build_features(sample_revenue_df)
        assert "volume_rolling_3m" in result.columns
        assert "volume_rolling_12m" in result.columns

    def test_output_has_seasonality(self, sample_revenue_df):
        result = build_features(sample_revenue_df)
        assert "month_sin" in result.columns
        assert "month_cos" in result.columns

    def test_no_nan_in_output(self, sample_revenue_df):
        result = build_features(sample_revenue_df)
        lag_cols = [c for c in result.columns if "lag_" in c or "rolling_" in c]
        assert result[lag_cols].isna().sum().sum() == 0

    def test_drops_early_rows(self, sample_revenue_df):
        result = build_features(sample_revenue_df)
        # Should drop the first 12 rows (longest lag)
        assert len(result) < len(sample_revenue_df)

    def test_price_index_near_one(self, sample_revenue_df):
        result = build_features(sample_revenue_df)
        # Price index should be near 1.0 for stable prices
        assert result["price_index"].mean() > 0.9
        assert result["price_index"].mean() < 1.1

    def test_mix_share_sums_to_one(self, sample_revenue_df):
        # Single product line, so mix share should be 1.0
        result = build_features(sample_revenue_df)
        assert all(abs(result["mix_share"] - 1.0) < 0.001)

    def test_seasonality_bounded(self, sample_revenue_df):
        result = build_features(sample_revenue_df)
        assert result["month_sin"].min() >= -1.0
        assert result["month_sin"].max() <= 1.0
        assert result["month_cos"].min() >= -1.0
        assert result["month_cos"].max() <= 1.0

    def test_no_future_leakage(self, sample_revenue_df):
        """Lag features should only use past data."""
        result = build_features(sample_revenue_df)
        # volume_lag_1 at row i should equal units_sold at row i-1
        for i in range(1, len(result)):
            row = result.iloc[i]
            prev_row = sample_revenue_df[
                (sample_revenue_df["month"] == row["month"] - pd.DateOffset(months=1))
            ]
            if len(prev_row) > 0:
                assert row["volume_lag_1"] == prev_row["units_sold"].values[0]
