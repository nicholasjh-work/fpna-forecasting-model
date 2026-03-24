-- Snowflake views exposing forecast outputs for dashboard consumption.
-- Tableau and Power BI connect to these views.

-- Forecast results view: actuals + forecast + scenarios in one table.
-- Grain: one row per division, product_line, month, scenario.
CREATE OR REPLACE VIEW reporting.v_forecast_results AS
SELECT
    division,
    product_line,
    month,
    net_revenue,
    'actual' AS record_type,
    'actual' AS scenario
FROM reporting.v_rpt_revenue_by_division

UNION ALL

SELECT
    division,
    product_line,
    forecast_month AS month,
    forecast_revenue AS net_revenue,
    'forecast' AS record_type,
    scenario
FROM forecast.forecast_output;

-- Forecast accuracy view: compares forecasted vs actual for past periods.
-- Used to track model performance over time.
CREATE OR REPLACE VIEW reporting.v_forecast_accuracy AS
WITH actuals AS (
    SELECT division, product_line, month, net_revenue AS actual_revenue
    FROM reporting.v_rpt_revenue_by_division
),
forecasts AS (
    SELECT division, product_line, forecast_month AS month, forecast_revenue
    FROM forecast.forecast_output
    WHERE scenario = 'base'
)
SELECT
    a.division,
    a.product_line,
    a.month,
    a.actual_revenue,
    f.forecast_revenue,
    a.actual_revenue - f.forecast_revenue AS forecast_error,
    ABS(a.actual_revenue - f.forecast_revenue) / NULLIF(a.actual_revenue, 0) AS abs_pct_error
FROM actuals a
JOIN forecasts f ON a.division = f.division
               AND a.product_line = f.product_line
               AND a.month = f.month;
