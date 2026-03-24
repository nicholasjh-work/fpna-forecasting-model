# FP&A Forecasting Model

**[Live Demo](https://nicholasjh-work.github.io/fpna-forecasting-model/)**

Driver-based and ML revenue forecasting framework for FP&A planning cycles. Linear regression model (MAPE 4.1%, WAPE 4.5%) outperformed the baseline last-value holdout (MAPE 6.9%) using time, volume, and price drivers. Exported standardized KPI metrics to Tableau executive dashboards. Designed for scenario and sensitivity analysis.

## What this solves

The FP&A team was forecasting revenue using spreadsheet-based models that relied on manual assumptions and last-period extrapolation. The models broke when seasonality shifted. They couldn't answer "what if volume drops 10% but price increases 5%" without rebuilding the spreadsheet. Forecast accuracy was around 7-8% MAPE, which meant the quarterly earnings narrative was frequently off.

This model automates the forecast using actual business drivers (volume trends, price changes, product mix shifts, seasonality) and produces scenario outputs that plug directly into the FP&A planning template and Tableau dashboards.

## Repo structure

```
fpna-forecasting/
  src/
    data_pull.py              Snowflake data extraction with parameterized SQL
    feature_engineering.py    Driver-based features: lag, rolling avg, seasonality, price index
    model.py                  Linear regression training, evaluation, cross-validation
    forecast.py               Generate forecasts with confidence intervals
    scenario.py               Sensitivity analysis: volume, price, mix scenarios
    export.py                 Export forecast KPIs to CSV for Tableau
  sql/
    extract_revenue.sql       Snowflake query for historical revenue by division, product, month
    extract_drivers.sql       Volume, price, and mix driver extraction
    forecast_views.sql        Snowflake views for forecast output consumption
  notebooks/
    eda.ipynb                 Exploratory data analysis with visualizations
    model_evaluation.ipynb    Model comparison, residual analysis, feature importance
  docs/
    model_spec.md             Model design, feature definitions, evaluation criteria
    kpi_definitions.md        Forecast KPI governance (MAPE, WAPE, bias)
    scenario_guide.md         How to run and interpret scenario analysis
  tests/
    test_features.py          Feature engineering unit tests
    test_model.py             Model training and prediction tests
    test_scenarios.py         Scenario output validation
    conftest.py               Shared fixtures with sample data
  config/
    model_config.yaml         Hyperparameters, feature list, train/test split
    scenarios.yaml            Predefined scenario definitions
  data/
    sample/
      sample_revenue.csv      Synthetic monthly revenue for testing
      sample_drivers.csv      Synthetic driver data
  models/
    (trained model artifacts saved here, gitignored)
  .env.example
  .gitignore
  requirements.txt
  README.md
```

## Model design

### Driver-based approach

Revenue is decomposed into three drivers:
- **Volume**: units sold per product per month
- **Price**: average selling price per unit
- **Mix**: proportion of revenue from each product line

The model predicts revenue as `volume * price`, adjusted for mix effects and seasonality.

### Features

| Feature | Description | Source |
|---|---|---|
| volume_lag_1 | Units sold last month | fact_revenue |
| volume_lag_3 | Units sold 3 months ago | fact_revenue |
| volume_rolling_3m | 3-month rolling average of units | fact_revenue |
| volume_rolling_12m | 12-month rolling average of units | fact_revenue |
| price_index | Current avg price / 12-month avg price | fact_revenue |
| price_change_pct | Month-over-month price change | fact_revenue |
| mix_share | Product line share of total revenue | fact_revenue |
| month_sin | Sine of month (captures seasonality) | dim_date |
| month_cos | Cosine of month (captures seasonality) | dim_date |
| is_q4 | Binary flag for Q4 (fiscal year-end effects) | dim_date |
| volume_yoy_change | Year-over-year volume change | fact_revenue |

Features are generated in `src/feature_engineering.py` using pandas and NumPy. No features require future data (all are lagged or rolling).

### Model

Linear regression from scikit-learn. Chosen for interpretability: FP&A teams need to explain the forecast to the CFO, and "the model says volume is the biggest driver at 0.73 coefficient" is a conversation they can have. A black-box model would not be accepted.

Evaluation:
- MAPE: 4.1% (vs. 6.9% baseline)
- WAPE: 4.5%
- Bias: +0.3% (slight over-forecast, acceptable)
- Cross-validation: 5-fold, MAPE range 3.8% to 4.6%

### Baseline

Last-value holdout: forecast = last month's actual revenue. This is the simplest model and the one the FP&A team was effectively using with their spreadsheets. MAPE 6.9%.

## Scenario analysis

The scenario module (`src/scenario.py`) takes a base forecast and applies shocks:

- **Volume shock**: multiply volume by a factor (e.g., 0.9 for 10% drop)
- **Price shock**: multiply price by a factor
- **Mix shift**: reallocate product mix percentages

Predefined scenarios are in `config/scenarios.yaml`:

```yaml
scenarios:
  base:
    volume_factor: 1.0
    price_factor: 1.0
  conservative:
    volume_factor: 0.92
    price_factor: 0.98
  optimistic:
    volume_factor: 1.08
    price_factor: 1.03
  price_increase:
    volume_factor: 1.0
    price_factor: 1.05
  volume_decline:
    volume_factor: 0.85
    price_factor: 1.0
```

Run with: `python -m src.scenario --scenario conservative`

## Export to Tableau

`src/export.py` writes forecast results to CSV in a format that Tableau can import directly. The output includes:

- Division, product line, month
- Actual revenue, forecasted revenue, variance
- Upper and lower confidence bounds (95%)
- Scenario label
- MAPE and WAPE per division

The Snowflake view in `sql/forecast_views.sql` exposes the same data for dashboards that connect directly to the warehouse.

## Getting started

```bash
git clone https://github.com/nicholasjh-work/fpna-forecasting-model.git
cd fpna-forecasting-model

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env  # fill in Snowflake credentials

# Pull data from Snowflake
python -m src.data_pull

# Generate features
python -m src.feature_engineering

# Train and evaluate
python -m src.model

# Generate forecast
python -m src.forecast

# Run scenario analysis
python -m src.scenario --scenario conservative

# Export for Tableau
python -m src.export

# Run tests
pytest tests/ -v
```

## Disclaimer

The model code and feature engineering in this repository reflect a forecasting system built for an enterprise FP&A team. The actual revenue data, division names, and proprietary driver logic from that engagement remain confidential. Sample data included here are synthetic.
