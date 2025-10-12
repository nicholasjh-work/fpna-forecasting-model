# Predictive FP&A Forecasting Model (Driver-Based + ML)

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
