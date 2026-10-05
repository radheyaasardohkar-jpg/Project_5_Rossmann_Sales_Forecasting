import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Rossmann Sales Forecasting",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

model_comparison = pd.read_csv(
    "outputs/model_comparison.csv"
)

future_forecast = pd.read_csv(
    "outputs/store_forecast_30_days.csv"
)

future_forecast["Date"] = pd.to_datetime(
    future_forecast["Date"]
)


# Load historical data for the selected store
historical_data = pd.read_csv(
    "data/train.csv"
)

historical_data["Date"] = pd.to_datetime(
    historical_data["Date"]
)

candidate_store = 551

store_history = (
    historical_data[
        historical_data["Store"] == candidate_store
    ]
    .sort_values("Date")
    .copy()
)


# ============================================================
# CALCULATE KPIs
# ============================================================

total_forecast_sales = (
    future_forecast["Forecasted_Sales"].sum()
)

average_forecast_sales = (
    future_forecast["Forecasted_Sales"].mean()
)

recent_average_sales = (
    store_history.tail(30)["Sales"].mean()
)

expected_change = (
    (average_forecast_sales - recent_average_sales)
    / recent_average_sales
) * 100

best_model = model_comparison.iloc[0]["Model"]

best_model_rmse = model_comparison.iloc[0]["RMSE"]

best_model_mape = model_comparison.iloc[0]["MAPE"]

naive_rmse = (
    model_comparison[
        model_comparison["Model"] == "Naive"
    ]["RMSE"].iloc[0]
)

rmse_improvement = (
    (naive_rmse - best_model_rmse)
    / naive_rmse
) * 100


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 Project Information")

st.sidebar.markdown(
    """
    **Project:** Rossmann Store Sales Forecasting

    **Forecast Horizon:** 30 Days

    **Forecast Store:** 551

    **Best Model:** Random Forest

    **Target:** Daily Sales

    **Evaluation:** MAE, RMSE, MAPE
    """
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    ### Models Evaluated

    - Naive Baseline
    - Linear Regression
    - Random Forest
    - SARIMA
    """
)

st.sidebar.divider()

st.sidebar.info(
    "Forecast assumptions: future Promo, SchoolHoliday "
    "and StateHoliday values are currently set to baseline "
    "assumptions."
)


# ============================================================
# HEADER
# ============================================================

st.title("📈 Rossmann Store Sales Forecasting")

st.markdown(
    """
    ### 30-Day Sales Forecast Dashboard

    This dashboard presents historical sales patterns,
    forecasting model performance, and the expected sales
    outlook for the selected Rossmann store.
    """
)

st.divider()


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📌 Forecast Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "30-Day Forecast Sales",
        f"{total_forecast_sales:,.0f}"
    )

with col2:
    st.metric(
        "Average Daily Forecast",
        f"{average_forecast_sales:,.0f}"
    )

with col3:
    st.metric(
        "Expected Change",
        f"{expected_change:+.2f}%"
    )

with col4:
    st.metric(
        "Best Model",
        best_model
    )


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.divider()

st.subheader("🤖 Model Performance")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Best Model RMSE",
        f"{best_model_rmse:,.0f}"
    )

    st.metric(
        "Best Model MAPE",
        f"{best_model_mape:.2f}%"
    )


with col2:

    st.metric(
        "RMSE Improvement vs Naive",
        f"{rmse_improvement:.2f}%"
    )

    st.markdown(
        f"""
        **Selected Model:** `{best_model}`

        The model was selected using chronological
        time-series evaluation rather than random
        train-test splitting.
        """
    )


# ============================================================
# HISTORICAL VS FORECAST
# ============================================================

st.divider()

st.subheader("📈 Historical Sales vs 30-Day Forecast")

recent_history = (
    store_history.tail(90)[
        ["Date", "Sales"]
    ]
    .rename(columns={"Sales": "Sales"})
)

historical_chart = px.line(
    recent_history,
    x="Date",
    y="Sales",
    title="Last 90 Days of Historical Sales"
)

historical_chart.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales",
    hovermode="x unified"
)

st.plotly_chart(
    historical_chart,
    use_container_width=True
)


forecast_chart = px.line(
    future_forecast,
    x="Date",
    y="Forecasted_Sales",
    title="Next 30 Days Forecast"
)

forecast_chart.update_layout(
    xaxis_title="Date",
    yaxis_title="Forecasted Sales",
    hovermode="x unified"
)

st.plotly_chart(
    forecast_chart,
    use_container_width=True
)


# ============================================================
# COMBINED HISTORICAL + FORECAST CHART
# ============================================================

st.subheader("🔮 Historical + Forecast Outlook")

historical_combined = (
    store_history.tail(90)[
        ["Date", "Sales"]
    ]
    .rename(columns={"Sales": "Value"})
)

historical_combined["Type"] = "Historical"

forecast_combined = (
    future_forecast[
        ["Date", "Forecasted_Sales"]
    ]
    .rename(columns={"Forecasted_Sales": "Value"})
)

forecast_combined["Type"] = "Forecast"

combined_data = pd.concat(
    [
        historical_combined,
        forecast_combined
    ],
    ignore_index=True
)

combined_chart = px.line(
    combined_data,
    x="Date",
    y="Value",
    color="Type",
    title="Historical Sales and Future Forecast"
)

combined_chart.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales",
    hovermode="x unified"
)

st.plotly_chart(
    combined_chart,
    use_container_width=True
)


# ============================================================
# MODEL COMPARISON CHART
# ============================================================

st.divider()

st.subheader("🏆 Model Comparison")

model_chart = px.bar(
    model_comparison,
    x="Model",
    y="RMSE",
    title="RMSE by Forecasting Model",
    text_auto=".0f"
)

model_chart.update_layout(
    xaxis_title="Model",
    yaxis_title="RMSE"
)

st.plotly_chart(
    model_chart,
    use_container_width=True
)

st.dataframe(
    model_comparison,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# WEEKDAY FORECAST PATTERN
# ============================================================

st.divider()

st.subheader("📅 Forecast by Day of Week")

future_forecast["Day_Name"] = (
    future_forecast["Date"].dt.day_name()
)

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

forecast_weekday_pattern = (
    future_forecast
    .groupby("Day_Name")["Forecasted_Sales"]
    .mean()
    .reindex(weekday_order)
    .reset_index()
)

forecast_weekday_pattern.columns = [
    "Day",
    "Average_Forecasted_Sales"
]

weekday_chart = px.bar(
    forecast_weekday_pattern,
    x="Day",
    y="Average_Forecasted_Sales",
    title="Average Forecasted Sales by Weekday",
    text_auto=".0f"
)

weekday_chart.update_layout(
    xaxis_title="Day of Week",
    yaxis_title="Average Forecasted Sales"
)

st.plotly_chart(
    weekday_chart,
    use_container_width=True
)


# ============================================================
# TOP AND LOW FORECAST DAYS
# ============================================================

st.divider()

st.subheader("📊 Highest and Lowest Forecast Days")

col1, col2 = st.columns(2)

top_forecast_days = (
    future_forecast
    .sort_values(
        "Forecasted_Sales",
        ascending=False
    )
    .head(5)
    [["Date", "Forecasted_Sales"]]
)

lowest_forecast_days = (
    future_forecast
    .sort_values(
        "Forecasted_Sales",
        ascending=True
    )
    .head(5)
    [["Date", "Forecasted_Sales"]]
)

with col1:

    st.markdown("### 🔝 Top 5 Forecast Days")

    st.dataframe(
        top_forecast_days,
        use_container_width=True,
        hide_index=True
    )


with col2:

    st.markdown("### 🔻 Lowest 5 Forecast Days")

    st.dataframe(
        lowest_forecast_days,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# RECENT VS FUTURE PERFORMANCE
# ============================================================

st.divider()

st.subheader("📊 Recent vs Expected Sales")

comparison_data = pd.DataFrame(
    {
        "Period": [
            "Last 30 Days",
            "Next 30 Days"
        ],
        "Average Daily Sales": [
            recent_average_sales,
            average_forecast_sales
        ]
    }
)

comparison_chart = px.bar(
    comparison_data,
    x="Period",
    y="Average Daily Sales",
    title="Average Daily Sales Comparison",
    text_auto=".0f"
)

comparison_chart.update_layout(
    xaxis_title="Period",
    yaxis_title="Average Daily Sales"
)

st.plotly_chart(
    comparison_chart,
    use_container_width=True
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Business Insights")

highest_day = (
    future_forecast.loc[
        future_forecast["Forecasted_Sales"].idxmax()
    ]
)

lowest_day = (
    future_forecast.loc[
        future_forecast["Forecasted_Sales"].idxmin()
    ]
)

highest_day_date = highest_day["Date"].strftime(
    "%d %b %Y"
)

lowest_day_date = lowest_day["Date"].strftime(
    "%d %b %Y"
)

highest_day_sales = highest_day[
    "Forecasted_Sales"
]

lowest_day_sales = lowest_day[
    "Forecasted_Sales"
]

insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    st.markdown(
        f"""
        **📈 Expected Demand**

        The model forecasts approximately
        **{total_forecast_sales:,.0f} sales units**
        over the next 30 days.

        Average expected daily sales are
        approximately **{average_forecast_sales:,.0f}**.
        """
    )

    st.markdown(
        f"""
        **🏆 Peak Forecast Day**

        The highest forecast is expected on
        **{highest_day_date}**, with approximately
        **{highest_day_sales:,.0f}** sales.
        """
    )


with insight_col2:

    st.markdown(
        f"""
        **📉 Lowest Forecast Day**

        The lowest forecast is expected on
        **{lowest_day_date}**, with approximately
        **{lowest_day_sales:,.0f}** sales.
        """
    )

    st.markdown(
        f"""
        **🤖 Model Reliability**

        Random Forest achieved a test MAPE of
        approximately **{best_model_mape:.2f}%**
        and improved RMSE over the Naive baseline
        by approximately **{rmse_improvement:.2f}%**.
        """
    )


# ============================================================
# BUSINESS RECOMMENDATIONS
# ============================================================

st.subheader("🎯 Business Recommendations")

st.markdown(
    """
    **1. Inventory Planning**

    Use the daily forecast to prepare inventory and
    replenishment levels ahead of expected high-demand days.

    **2. Staff Planning**

    Allocate additional staff and operational resources
    around higher forecasted sales periods.

    **3. Promotion Planning**

    Future forecasts can be improved by incorporating
    known promotional calendars and holiday information.

    **4. Continuous Monitoring**

    Compare actual sales against forecasted sales regularly
    and retrain the model when performance deteriorates.

    **5. Forecast Enhancement**

    A production version should incorporate future-known
    promotions, school holidays, state holidays and other
    calendar events rather than relying on baseline assumptions.
    """
)


# ============================================================
# FORECAST DATA
# ============================================================

st.divider()

st.subheader("📋 Complete 30-Day Forecast")

st.dataframe(
    future_forecast,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD BUTTON
# ============================================================

csv_data = future_forecast.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download 30-Day Forecast CSV",
    data=csv_data,
    file_name="store_551_30_day_forecast.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Rossmann Sales Forecasting | "
    "Time Series Forecasting Portfolio Project"
)