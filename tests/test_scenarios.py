"""Tests for scenario analysis."""
import pytest
import pandas as pd

from src.scenario import apply_scenario, load_scenarios


@pytest.fixture
def sample_forecast():
    return pd.DataFrame({
        "month": pd.date_range("2025-01-01", periods=3, freq="MS"),
        "forecast_revenue": [1000000.0, 1050000.0, 1100000.0],
        "lower_bound_95": [900000.0, 950000.0, 1000000.0],
        "upper_bound_95": [1100000.0, 1150000.0, 1200000.0],
        "residual_std": [50000.0, 50000.0, 50000.0],
    })


class TestApplyScenario:
    def test_base_scenario_unchanged(self, sample_forecast):
        result = apply_scenario(sample_forecast, 1.0, 1.0, "base")
        assert list(result["forecast_revenue"]) == [1000000.0, 1050000.0, 1100000.0]

    def test_volume_drop_reduces_revenue(self, sample_forecast):
        result = apply_scenario(sample_forecast, 0.9, 1.0, "vol_drop")
        assert all(result["forecast_revenue"] < sample_forecast["forecast_revenue"])

    def test_price_increase_raises_revenue(self, sample_forecast):
        result = apply_scenario(sample_forecast, 1.0, 1.05, "price_up")
        assert all(result["forecast_revenue"] > sample_forecast["forecast_revenue"])

    def test_combined_shock(self, sample_forecast):
        result = apply_scenario(sample_forecast, 0.9, 1.1, "combined")
        expected_factor = 0.9 * 1.1  # 0.99
        expected = sample_forecast["forecast_revenue"] * expected_factor
        assert abs(result["forecast_revenue"].iloc[0] - expected.iloc[0]) < 1

    def test_scenario_label_set(self, sample_forecast):
        result = apply_scenario(sample_forecast, 0.9, 1.0, "conservative")
        assert all(result["scenario"] == "conservative")

    def test_load_scenarios_returns_dict(self):
        scenarios = load_scenarios()
        assert isinstance(scenarios, dict)
        assert "base" in scenarios
