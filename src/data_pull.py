"""
Pull historical revenue and driver data from Snowflake.

Extracts monthly revenue by division and product line with volume,
price, and mix components. Parameterized SQL, no string concatenation.

Usage:
    python -m src.data_pull
    python -m src.data_pull --months 36
"""
import argparse
import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

REVENUE_SQL = """
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
  AND dt.calendar_date >= DATEADD('month', -%s, CURRENT_DATE)
GROUP BY d.division, p.product_line, DATE_TRUNC('month', dt.calendar_date)
ORDER BY d.division, p.product_line, month
"""

OUTPUT_DIR = Path(__file__).parent.parent / "data"


def pull_data(months: int = 36) -> pd.DataFrame:
    """Pull revenue data from Snowflake."""
    from snowflake.connector import connect

    conn = connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        database=os.getenv("SNOWFLAKE_DATABASE", "FINANCE_DW"),
        schema=os.getenv("SNOWFLAKE_SCHEMA", "REPORTING"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "ANALYTICS_WH"),
    )

    logger.info("Pulling %d months of revenue data from Snowflake", months)
    df = pd.read_sql(REVENUE_SQL, conn, params=[months])
    conn.close()

    logger.info("Pulled %d rows", len(df))
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--months", type=int, default=36, help="Months of history to pull")
    args = parser.parse_args()

    try:
        df = pull_data(args.months)
    except ImportError:
        logger.warning("Snowflake connector not installed. Using sample data.")
        sample_path = OUTPUT_DIR / "sample" / "sample_revenue.csv"
        if sample_path.exists():
            df = pd.read_csv(sample_path, parse_dates=["month"])
            logger.info("Loaded %d rows from sample data", len(df))
        else:
            logger.error("No sample data found at %s", sample_path)
            return
    except Exception as e:
        logger.error("Snowflake pull failed: %s", e)
        return

    output_path = OUTPUT_DIR / "revenue_history.csv"
    df.to_csv(output_path, index=False)
    logger.info("Saved to %s", output_path)


if __name__ == "__main__":
    main()
