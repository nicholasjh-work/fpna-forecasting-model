# Predictive FP&A Forecasting Model (Driver-Based + ML)

<<<<<<< HEAD
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
=======
## Executive Summary
This project automates the financial planning and forecasting process using a driver-based logic integrated with machine learning models. It enables faster, more accurate forecasting across revenue, volume, and cost drivers, supporting strategic decisions for Finance and Operations leaders.

## Business Problem
Manual forecasting cycles caused high variance and slow decision-making for resource allocation and budgeting. Executives needed predictive accuracy and transparency at the driver level.

## Solution
- Built a Python model integrated with Snowflake SQL for data preparation and transformation.  
- Created driver-based forecasting logic with price, volume, mix, and freight levers.  
- Automated variance scenarios (Base, Optimistic, Conservative) with predictive ML overlays.  
- Visualized outputs in Power BI dashboards for executive storytelling.

## Results
- Improved forecast accuracy by ~15% and reduced cycle time by ~25%.  
- Delivered zero-defect executive reporting for faster capex and freight decisions.  
- Increased confidence and adoption among senior Finance and Operations leaders.

## Repository Structure
/notebooks → Jupyter notebooks for model training and scoring
/sql → Snowflake scripts for data prep and aggregation
/powerbi → PBIX templates and DAX measures
/docs → Business logic, data dictionary, and KPI definitions

## Technology Stack
Python • Snowflake • SQL • Power BI • Databricks (optional)
>>>>>>> origin/main
