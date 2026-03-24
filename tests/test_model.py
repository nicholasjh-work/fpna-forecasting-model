"""Tests for model training and evaluation."""
import pytest
import numpy as np

from src.model import train_evaluate, FEATURE_COLS


class TestTrainEvaluate:
    def test_returns_mape(self, sample_features_df):
        if len(sample_features_df) < 10:
            pytest.skip("Not enough rows after feature engineering")
        results, model = train_evaluate(sample_features_df)
        assert "mape" in results
        assert results["mape"] >= 0

    def test_mape_below_threshold(self, sample_features_df):
        if len(sample_features_df) < 10:
            pytest.skip("Not enough rows")
        results, _ = train_evaluate(sample_features_df)
        # On synthetic data with clear trend, MAPE should be reasonable
        assert results["mape"] < 50  # loose bound for synthetic data

    def test_returns_feature_importance(self, sample_features_df):
        if len(sample_features_df) < 10:
            pytest.skip("Not enough rows")
        results, _ = train_evaluate(sample_features_df)
        assert "feature_importance" in results
        assert len(results["feature_importance"]) == len(FEATURE_COLS)

    def test_importance_sums_near_one(self, sample_features_df):
        if len(sample_features_df) < 10:
            pytest.skip("Not enough rows")
        results, _ = train_evaluate(sample_features_df)
        total = sum(fi["importance"] for fi in results["feature_importance"])
        assert abs(total - 1.0) < 0.01

    def test_cv_mapes_returned(self, sample_features_df):
        if len(sample_features_df) < 10:
            pytest.skip("Not enough rows")
        results, _ = train_evaluate(sample_features_df)
        assert "cv_mapes" in results
        assert len(results["cv_mapes"]) == 5

    def test_model_has_coefficients(self, sample_features_df):
        if len(sample_features_df) < 10:
            pytest.skip("Not enough rows")
        _, model = train_evaluate(sample_features_df)
        assert hasattr(model, "coef_")
        assert len(model.coef_) == len(FEATURE_COLS)
