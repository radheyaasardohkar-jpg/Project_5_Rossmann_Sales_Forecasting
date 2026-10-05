# Rossmann Store Sales Forecasting

## 📌 Project Overview

This project focuses on forecasting daily sales for a Rossmann retail store using historical sales data and time-series forecasting techniques.

The objective is to understand historical sales patterns, engineer time-based and lag features, compare multiple forecasting approaches, select the best-performing model, and generate a 30-day sales forecast that can support business planning.

> **Project Type:** Portfolio / Analytical Forecasting Project
> **Dataset:** Rossmann Store Sales
> **Forecast Horizon:** 30 Days
> **Selected Store:** Store 551
> **Best Model:** Random Forest Regressor

---

## 🎯 Business Problem

Retail businesses need reliable sales forecasts to support:

* Inventory planning
* Staff allocation
* Promotion planning
* Operational resource planning
* Demand monitoring

The goal of this project is to use historical sales behavior to estimate future daily sales and compare different forecasting approaches.

---

## 📊 Dataset

The project uses the **Rossmann Store Sales** dataset.

The main datasets contain:

* Daily store sales
* Customer counts
* Store opening status
* Promotions
* State holidays
* School holidays
* Store characteristics

The raw dataset is not included in this repository.

---

## 🔎 Exploratory Data Analysis

The analysis examined:

* Overall sales trends
* Daily sales patterns
* Monthly sales trends
* Year-over-year sales behavior
* Day-of-week seasonality
* Store-level sales performance
* Rolling averages
* Store closures
* Sales distribution
* Representative store behavior

Time-series analysis showed that sales are influenced by calendar patterns, weekly seasonality, promotions, holidays, and store operating status.

---

## 🛠️ Feature Engineering

The forecasting models used time-based and historical sales features.

### Calendar Features

* Year
* Month
* Day
* Day of Week
* Week of Year
* Quarter

### Business Features

* Promotion
* School Holiday
* State Holiday
* Store Open/Closed status

### Lag Features

* Lag 1 day
* Lag 7 days
* Lag 14 days
* Lag 28 days

### Rolling Features

* 7-day rolling mean
* 14-day rolling mean
* 30-day rolling mean

Rolling features were calculated using shifted historical sales to avoid future-data leakage.

---

## 🧪 Forecasting Strategy

A chronological train-validation-test split was used instead of random splitting.

The data was divided approximately into:

* **70% Training**
* **15% Validation**
* **15% Testing**

This preserves the temporal order of observations and better represents how forecasting models are used in real-world scenarios.

---

## 🤖 Models Compared

Four forecasting approaches were evaluated:

### 1. Naive Baseline

Uses the previous day's sales as the prediction.

### 2. Linear Regression

Uses calendar, promotion, holiday, lag, and rolling features to model sales.

### 3. Random Forest Regressor

Captures nonlinear relationships between historical sales behavior and engineered features.

### 4. SARIMA

A classical statistical time-series model incorporating seasonal behavior.

---

## 📏 Evaluation Metrics

The models were evaluated using:

* **MAE** — Mean Absolute Error
* **RMSE** — Root Mean Squared Error
* **MAPE** — Mean Absolute Percentage Error

MAPE was calculated excluding days where actual sales were zero, since zero actual values make percentage error undefined.

---

## 🏆 Model Results

| Model             |        MAE |       RMSE |      MAPE |
| ----------------- | ---------: | ---------: | --------: |
| **Random Forest** | **557.50** | **910.09** | **9.01%** |
| Linear Regression |     744.92 |   1,158.45 |    11.29% |
| SARIMA            |   1,073.87 |   1,644.30 |    14.99% |
| Naive             |   2,835.76 |   4,038.31 |    32.60% |

### Best Model

**Random Forest** achieved the best overall performance among the evaluated models.

Its test performance was:

* **MAE:** 557.50
* **RMSE:** 910.09
* **MAPE:** 9.01%

The Random Forest model substantially outperformed the Naive baseline, demonstrating the value of combining calendar information with historical sales features.

---

## 🔮 30-Day Forecast

The selected Random Forest model was used to generate a recursive 30-day forecast for Store 551.

The forecast output is available in:

```text
outputs/store_forecast_30_days.csv
```

The forecast contains:

* Date
* Forecasted Sales

The current portfolio implementation uses baseline assumptions for future promotional and holiday variables.

---

## 💡 Business Insights

The forecasting analysis can support several business decisions:

### Inventory Planning

Expected higher-sales periods can be used to prepare inventory and replenishment levels.

### Staff Planning

Store staffing can be adjusted based on expected demand.

### Promotion Planning

Historical promotional behavior can help identify opportunities for future campaigns.

### Operational Planning

Forecasted demand can support short-term operational resource allocation.

### Continuous Monitoring

Actual sales should be compared with forecasted sales regularly to monitor model performance.

---

## 📊 Dashboard

A Streamlit dashboard was created to present the forecasting results interactively.

The dashboard includes:

* Forecast KPIs
* Historical sales trends
* Historical vs forecast visualization
* Model comparison
* Weekday forecast patterns
* Highest forecast days
* Lowest forecast days
* Recent vs expected sales
* Business recommendations
* Forecast CSV download

Run the dashboard with:

```bash
streamlit run app.py
```

---

## 🧰 Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* Statsmodels
* Plotly
* Streamlit
* Jupyter Notebook

---

## 📁 Project Structure

```text
Project_5_Rossmann_Sales_Forecasting/
│
├── data/
│   └── Raw Kaggle datasets
│
├── notebooks/
│   └── 01_data_understanding.ipynb
│
├── src/
│
├── outputs/
│   ├── model_comparison.csv
│   └── store_forecast_30_days.csv
│
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/radheyaasardohkar-jpg/Project_5_Rossmann_Sales_Forecasting.git
cd Project_5_Rossmann_Sales_Forecasting
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Add the dataset

Download the Rossmann Store Sales dataset from Kaggle and place the required CSV files inside:

text
data/


### 6. Run the notebook

Open:

notebooks/01_data_understanding.ipynb


and execute the analysis cells.

### 7. Run the dashboard


streamlit run app.py


---

## ⚠️ Limitations

This project is intended as a portfolio forecasting analysis rather than a production forecasting system.

Important limitations include:

* Forecasting was demonstrated on one representative store.
* Future promotion and holiday variables use baseline assumptions.
* The model is not connected to a live sales system.
* Forecasts are generated for a fixed 30-day horizon.
* Production deployment would require automated data pipelines and continuous model monitoring.

A production system could improve the approach by incorporating future-known promotions, holidays, richer store information, automated retraining, and live forecast monitoring.

---

## 📌 Key Takeaways

This project demonstrates an end-to-end time-series forecasting workflow:

```text
Data Loading
     ↓
Data Cleaning
     ↓
Exploratory Data Analysis
     ↓
Time-Series Feature Engineering
     ↓
Chronological Train/Validation/Test Split
     ↓
Baseline Forecasting
     ↓
Multiple Model Training
     ↓
Model Evaluation
     ↓
Model Comparison
     ↓
Best Model Selection
     ↓
30-Day Forecast
     ↓
Business Insights
     ↓
Interactive Dashboard


The main finding was that the **Random Forest model outperformed the Naive, Linear Regression, and SARIMA approaches on the test set for the selected store**.

---

## 👤 Author ##

RADHEYA AMOL ASARDOHKAR

Data Science Portfolio Project — Time Series Forecasting
