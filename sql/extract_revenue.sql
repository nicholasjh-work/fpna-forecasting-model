-- Revenue extraction for the forecasting model.
-- Pulls monthly revenue by division and product line with volume and price drivers.
-- Grain: one row per division, product_line, month.

SELECT
    d.division,
    p.product_line,
    DATE_TRUNC('month', dt.calendar_date) AS month,
    SUM(f.quantity)                        AS units_sold,
    SUM(f.net_amount)                      AS net_revenue,
    SUM(f.cogs)                            AS cogs,
    CASE
        WHEN SUM(f.quantity) = 0 THEN 0
        ELSE SUM(f.net_amount) / SUM(f.quantity)
    END                                    AS avg_price,
    COUNT(DISTINCT f.customer_id)          AS active_customers
FROM fact_revenue f
JOIN dim_division d   ON f.division_id = d.division_id
JOIN dim_product p    ON f.product_id = p.product_id
JOIN dim_date dt      ON f.date_key = dt.date_key
WHERE f.is_intercompany = FALSE
  AND f.is_test_data = FALSE
  AND dt.calendar_date >= DATEADD('month', -36, CURRENT_DATE)
GROUP BY d.division, p.product_line, DATE_TRUNC('month', dt.calendar_date)
ORDER BY d.division, p.product_line, month;
