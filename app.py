import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def plot_pr_graph(df, start_date=None, end_date=None):
    if start_date:
        df = df[df["Date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["Date"] <= pd.to_datetime(end_date)]

    if df.empty:
        return None

    df = df.sort_values("Date").reset_index(drop=True)

    df["PR_MA30"] = df["PR"].rolling(30).mean()

    start_value = 73.9
    start_date_budget = df["Date"].min()
    budget_values = []
    for d in df["Date"]:
        days_passed = (d - start_date_budget).days
        years_passed = days_passed / 365.25
        budget_pr = start_value * ((1 - 0.008) ** years_passed)
        budget_values.append(budget_pr)
    df["Budget_PR"] = budget_values

    def get_color(ghi):
        if ghi < 2: return "navy"
        elif ghi < 4: return "lightblue"
        elif ghi < 6: return "orange"
        else: return "brown"
    colors = df["GHI"].apply(get_color)

    fig, ax = plt.subplots(figsize=(14, 7))

    ax.scatter(df["Date"], df["PR"], c=colors, s=15, alpha=0.7, label="Daily PR")
    ax.plot(df["Date"], df["PR_MA30"], color="red", linewidth=2, label="30-d moving avg of PR")
    ax.plot(df["Date"], df["Budget_PR"], color="green", linewidth=2, label="Target Budget Yield Performance Ratio")

    pct_above = (df["PR"] > df["Budget_PR"]).mean() * 100
    ax.text(0.02, 0.92, f"Points above Target Budget PR = {pct_above:.1f}%",
            transform=ax.transAxes, fontsize=11, bbox=dict(facecolor="white", alpha=0.6))

    ax.set_title(f"Performance Ratio Evolution\nFrom {df['Date'].min().date()} to {df['Date'].max().date()}",
                 fontsize=14)
    ax.set_ylabel("Performance Ratio (PR) [%]")
    ax.set_xlabel("Date")

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
    plt.xticks(rotation=0)

    ax.legend(loc="upper right")

    stats = {
        "last 7d": df["PR"].tail(7).mean(),
        "last 30d": df["PR"].tail(30).mean(),
        "last 60d": df["PR"].tail(60).mean(),
        "last 180d": df["PR"].tail(180).mean(),
        "last 365d": df["PR"].tail(365).mean(),
        "lifetime": df["PR"].mean()
    }
    textstr = "\n".join([f"Average PR {k}: {v:.1f} %" for k, v in stats.items()])
    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
    ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment="bottom", horizontalalignment="right", bbox=props)

    plt.tight_layout()
    
    return fig

st.set_page_config(layout="wide")
st.title("Performance Ratio (PR) Analysis")

@st.cache_data
def load_data(filepath="processed_data.csv"):
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

data = load_data()

st.sidebar.header("Filter by Date")

min_date = data["Date"].min().date()
max_date = data["Date"].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

pr_figure = plot_pr_graph(data, start_date, end_date)
st.pyplot(pr_figure)
