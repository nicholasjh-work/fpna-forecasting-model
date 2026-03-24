# Forecast KPI Definitions

Governed definitions for the metrics used to evaluate forecast quality.

## MAPE (Mean Absolute Percentage Error)

**Business purpose:** Primary accuracy metric. Measures how far off the forecast is from actuals, expressed as a percentage.

**Formula:** `MEAN(ABS(actual - forecast) / actual) * 100`

**Calculation grain:** Per division, product line, month.

**Reporting grain:** Rolled up to division or total. The roll-up uses WAPE, not averaged MAPE, because MAPE overweights small-revenue segments.

**Inclusions:** All months with both actual and forecast values.

**Exclusions:** Months where actual revenue is zero (division-by-zero). These are excluded from MAPE but counted in the bias metric.

**Owner:** FP&A. Evaluated monthly after close.

**Caveats:** MAPE penalizes over-forecasts and under-forecasts equally. If the business cares more about one direction (e.g., under-forecasting is worse because it leads to underspending), use a directional metric alongside MAPE.

**Governance risk:** If someone calculates MAPE at the total company level instead of averaging across segments, large segments dominate. Always report both segment-level and total.

## WAPE (Weighted Absolute Percentage Error)

**Business purpose:** Revenue-weighted accuracy. Large-revenue segments contribute more to the score. Better than MAPE for aggregate reporting.

**Formula:** `SUM(ABS(actual - forecast)) / SUM(actual) * 100`

**Calculation grain:** Computed across all rows in the evaluation set.

**Reporting grain:** Total or by division.

**Caveats:** WAPE can look good even if small segments are badly forecast, as long as large segments are accurate. Review segment-level MAPE alongside WAPE.

## Forecast Bias

**Business purpose:** Measures systematic over- or under-forecasting. A model with low MAPE but high bias consistently leans one direction.

**Formula:** `MEAN(forecast - actual) / MEAN(actual) * 100`

**Interpretation:** Positive = over-forecast (predicting too high). Negative = under-forecast.

**Threshold:** Acceptable bias is between -3% and +3%. Outside this range, the model has a systematic lean that should be investigated.

**Caveats:** Bias can be near zero while individual segments have large opposing biases that cancel out. Check bias at the segment level too.
