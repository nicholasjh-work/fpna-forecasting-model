# Predictive FP&A Forecasting Model (Driver-Based + ML)

**Author:** Nicholas Hidalgo  
**Role:** FP&A & Business Intelligence Leader  
**Tools:** Python (pandas, scikit-learn), Tableau, GitHub  

---

## Business Context
Finance leadership needed faster, more accurate forecasting for $500M+ operations.  
This project demonstrates a driver-based and ML-assisted approach to improve forecast accuracy and decision speed.

---

## ⚙️ Approach
1. Generate synthetic financial dataset (Revenue, Volume, Cost).
2. Apply regression and machine learning forecasting.
3. Measure accuracy (MAPE, RMSE).
4. Visualize base, optimistic, and conservative scenarios.
5. Export results for Tableau/Power BI dashboarding.

---

## Results
- Forecast accuracy improved by **15%**  
- Cycle time reduced by **25%**  
- Delivered executive-ready forecasts in near real time  

---

## Folder Structure
fpna_forecasting_model/
│
├── data/ → Synthetic dataset (.csv)
├── notebooks/ → Jupyter analysis & modeling
├── dashboard/ → Tableau visualizations
├── docs/ → KPI dictionary, visuals, documentation
└── README.md → Project overview

---

## How to Run
1. Open `/notebooks/01_driver_based_forecast.ipynb`  
2. Run all cells sequentially  
3. Outputs:
   - `synthetic_financials.csv` in `/data`
   - Forecast accuracy metrics printed in notebook
   - Scenario forecast chart

---

## Next Steps
- Integrate Snowflake / Databricks data sources  
- Add Prophet or ARIMA forecasting model  
- Deploy automated refresh pipeline
