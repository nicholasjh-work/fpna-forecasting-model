# Model Specification

## Objective

Forecast monthly revenue by division and product line for FP&A planning cycles. Replace the spreadsheet-based last-value extrapolation with a driver-based model that captures volume trends, price changes, product mix, and seasonality.

## Model choice

Linear regression. Chosen for interpretability. The FP&A team presents forecast assumptions to the CFO and board. They need to say "the model weights volume at 0.73 and price at 0.18" and have that mean something. A gradient-boosted model would likely improve MAPE by 0.5-1 percentage point, but the team rejected it because they could not explain the forecast to a non-technical audience.

## Features

All features are backward-looking. No feature uses future data.

| Feature | Calculation | Why it matters |
|---|---|---|
| volume_lag_1 | Units sold last month | Most recent demand signal |
| volume_lag_3 | Units sold 3 months ago | Captures quarterly patterns |
| volume_rolling_3m | 3-month average of units | Smooths monthly noise |
| volume_rolling_12m | 12-month average of units | Captures annual baseline |
| price_index | Current price / 12-month avg price | Detects price drift |
| price_change_pct | Month-over-month price change | Captures pricing actions |
| mix_share | Product revenue / division revenue | Product mix effect |
| month_sin, month_cos | Cyclical month encoding | Seasonality without discontinuity |
| is_q4 | Binary Q4 flag | Fiscal year-end spending effects |
| volume_yoy_pct | Year-over-year volume change | Trend direction |

## Training

80/20 time-ordered split. No shuffle. The last 20% of months are the test set. This simulates the real use case: train on history, predict forward.

Cross-validation uses TimeSeriesSplit with 5 folds. Each fold trains on all data before the fold and tests on the fold. This avoids future leakage in the CV.

## Evaluation metrics

| Metric | Value | Baseline | Notes |
|---|---|---|---|
| MAPE | 4.1% | 6.9% | 41% improvement over baseline |
| WAPE | 4.5% | N/A | Weighted by actual revenue |
| Bias | +0.3% | N/A | Slight over-forecast. Acceptable. |
| CV MAPE | 3.8% to 4.6% | N/A | Stable across folds |

Baseline is last-value holdout: forecast = previous month actual.

## Confidence intervals

95% intervals based on residual standard deviation from the training set. Assumes normally distributed errors, which is approximately true for revenue at the division-month grain.

## Known limitations

The model assumes the relationship between drivers and revenue is linear and stationary. If the business enters a fundamentally different regime (acquisition, product discontinuation, market disruption), the model will underperform until retrained on the new data.

Seasonality is encoded as sine/cosine of the month number. This captures a single annual cycle. If the business has sub-annual cycles (bi-weekly payroll effects, holiday-specific patterns), the model won't capture them.

The model trains on division-product-month grain. It cannot forecast at the customer level or the weekly level without structural changes.
