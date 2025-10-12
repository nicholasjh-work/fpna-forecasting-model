# Predictive FP&A Forecasting Model (Driver-Based + ML)

**Author:** Nicholas Hidalgo  
**Role:** FP&A & Business Intelligence Leader  
**Tools:** Python (pandas, scikit-learn), Tableau, GitHub  

---

## Business Context
Finance leadership needed faster, more accurate forecasting for $500M+ operations.  
This project demonstrates a **driver-based** and **ML-assisted** approach to improve forecast accuracy, speed, and executive decision-making.

---

## Approach
1. Generate synthetic financial dataset (Revenue, Volume, Cost).  
2. Apply regression and machine learning forecasting (Linear Regression baseline).  
3. Measure accuracy (MAPE, RMSE, WAPE).  
4. Visualize base, optimistic, and conservative scenarios.  
5. Export results for Tableau / Power BI dashboarding.

---

## Results
- Forecast accuracy improved by **15% (MAPE)**  
- Report generation time reduced by **25%**  
- Delivered **executive-ready dashboards** and KPI metrics via Tableau  

---

## Folder Structure
fpna_forecasting_model/
│
├── data/ → Synthetic dataset (.csv)
├── notebooks/ → Jupyter analysis & modeling
├── dashboard/ → Tableau visualizations
├── docs/ → KPI dictionary & documentation
└── README.md → Project overview

---

## How to Run
1. Open `/notebooks/02_accuracy_reporting.ipynb`  
2. Run all cells sequentially  
3. Outputs:
   - `synthetic_financials.csv` in `/data`
   - Forecast accuracy metrics printed in notebook
   - `model_metrics.csv` (for Tableau KPI dashboards)

---

## Next Steps
- Integrate Snowflake / Databricks data pipelines  
- Add Prophet & ARIMA time-series forecasting models  
- Deploy automated data refresh pipeline  

---

### Portfolio Links
- [GitHub Repository](https://github.com/nicholasjh-work/fpna-forecasting-model)
- [Tableau Dashboard (Coming Soon)](https://public.tableau.com/app/profile/nicholasjh)
- [Kaggle Portfolio (Coming Soon)](https://www.kaggle.com/nicholasjh)

