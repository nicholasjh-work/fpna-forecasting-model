# FP&A Forecasting Model – Driver-Based + ML Approach

**Author:** Nicholas Hidalgo  
**Location:** Boston, MA  
**Role:** Business Intelligence & Analytics Leader  
**Tools:** Python • Pandas • scikit-learn • Matplotlib • Tableau • Power BI • Snowflake • Databricks  

---

## Executive Summary
This project demonstrates an **FP&A forecasting framework** that integrates traditional driver-based forecasting with **machine learning (Linear Regression)** to enhance revenue accuracy and decision-making efficiency.  

Developed as part of a modern analytics portfolio, this model automates baseline vs. ML forecast comparison, evaluates accuracy (MAPE, WAPE, RMSE), and exports KPI metrics for **Tableau executive dashboards**.

---

## Project Structure
fpna_forecasting_model/
│
├── data/ # Raw & processed datasets (CSV exports)
├── notebooks/ # Jupyter notebooks (modeling, accuracy, scenario analysis)
├── docs/ # Visuals & documentation (for README & Tableau)
├── dashboard/ # Tableau dashboard assets
├── README.md # Project documentation
└── requirements.txt # Environment dependencies

---

## Objectives
- Develop a **baseline & ML forecasting model** for revenue prediction  
- Quantify accuracy using MAPE, WAPE, and RMSE  
- Export standardized KPI metrics for Tableau  
- Visualize results for executive reporting  
- Build future scenario & sensitivity analysis (next phase)  

---

## Key Model Metrics (Sample Output)

| Model                    | MAPE   | WAPE   | RMSE  |
|---------------------------|--------|--------|-------:|
| Baseline (Last Value)     | 6.9%   | 7.3%   | 3,210 |
| ML Linear Regression      | 4.1%   | 4.5%   | 2,540 |

*Metrics calculated using test set from baseline vs. ML forecast comparison.*

---

## Forecast Visualization
A visual comparison of actual vs. forecasted revenue using a driver-based and ML model.

<p align="center">
  <img src="https://raw.githubusercontent.com/nicholasjh-work/fpna-forecasting-model/main/docs/actuals_vs_forecasts.png" alt="Forecast Comparison" width="750"/>
</p>

### Interpretation
- **Baseline:** Holds the last observed revenue constant.  
- **ML model:** Predicts revenue using time, volume, and price drivers.  
- ML model tracks actuals more closely → higher predictive accuracy.  
- Metrics exported to `data/model_metrics.csv` for Tableau dashboards.  

---

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/nicholasjh-work/fpna-forecasting-model.git
   cd fpna-forecasting-model

---

## Objectives
- Develop a **baseline & ML forecasting model** for revenue prediction  
- Quantify accuracy using MAPE, WAPE, and RMSE  
- Export standardized KPI metrics for Tableau  
- Visualize results for executive reporting  
- Build future scenario & sensitivity analysis (next phase)  

---

## Key Model Metrics (Sample Output)

| Model                    | MAPE   | WAPE   | RMSE  |
|---------------------------|--------|--------|-------:|
| Baseline (Last Value)     | 6.9%   | 7.3%   | 3,210 |
| ML Linear Regression      | 4.1%   | 4.5%   | 2,540 |

*Metrics calculated using test set from baseline vs. ML forecast comparison.*

---

## Forecast Visualization
A visual comparison of actual vs. forecasted revenue using a driver-based and ML model.

<p align="center">
  <img src="https://raw.githubusercontent.com/nicholasjh-work/fpna-forecasting-model/main/docs/actuals_vs_forecasts.png" alt="Forecast Comparison" width="750" />
</p>

### Interpretation
- **Baseline model:** Holds the last observed revenue constant.  
- **ML model (Linear Regression):** Predicts revenue using time, volume, and price drivers.  
- The **ML forecast** tracks actuals more closely, showing higher predictive accuracy and responsiveness to business drivers.  
- Exported metrics (`MAPE`, `WAPE`, `RMSE`) are stored in `data/model_metrics.csv` for Tableau or Power BI dashboards.

---

## Portfolio Links

| Platform | Link |
|-----------|------|
| **GitHub** | [nicholasjh-work](https://github.com/nicholasjh-work) |
| **Tableau Public** | [Nicholas Hidalgo](https://public.tableau.com/app/profile/nicholashidalgo) |
| **Kaggle** | [nicholasjhidalgo](https://www.kaggle.com/nicholashidalgo) |
| **LinkedIn** | [nicholasjhidalgo](https://www.linkedin.com/in/nicholasjhidalgo) |

---

## ⚙️ How to Run Locally

Follow these steps to reproduce the forecasting results and generate outputs for Tableau or Power BI.

### Clone the repository
```bash
git clone https://github.com/nicholasjh-work/fpna-forecasting-model.git
cd fpna-forecasting-model
```

```bash
python -m venv venv
source venv/bin/activate   # On macOS / Linux
venv\Scripts\activate      # On Windows
```


```bash
pip install -r requirements.txt
```

```bash
jupyter lab
```

```bash
notebooks/02_accuracy_reporting.ipynb
```

---

## This notebook will:
Generate baseline and ML forecasts
Compute accuracy metrics (MAPE, WAPE, RMSE)
Export outputs to data/model_metrics.csv
Save forecast visualization to docs/actuals_vs_forecasts.png

## Optional: Explore in Tableau
You can connect Tableau to:
data/model_metrics.csv for KPI metrics
data/synthetic_financials.csv for scenario visualization

## These datasets power executive dashboards for FP&A insights.

---
