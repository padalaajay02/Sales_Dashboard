import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Performance Dashboard")

@st.cache_data
def load_data():
    np.random.seed(42)
    n = 1000
    data = {
        "OrderID": np.arange(1000, 1000 + n),
        "OrderDate": pd.date_range(start="2023-01-01", periods=n, freq="D"),
        "Region": np.random.choice(["North", "South", "East", "West"], n),
        "Category": np.random.choice(["Technology", "Furniture", "Office Supplies"], n),
        "Product": np.random.choice(
            ["Laptop", "Phone", "Chair", "Table", "Pen", "Notebook", "Tablet"], n
        ),
        "Sales": np.random.randint(20, 2000, n),
        "Quantity": np.random.randint(1, 10, n),
    }

    df = pd.DataFrame(data)
    df["Profit"] = (df["Sales"] * np.random.uniform(0.1, 0.3, n)).round(2)
    df["CustomerSegment"] = np.random.choice(
        ["Consumer", "Corporate", "Home Office"], n
    )

    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    return df

df = load_data()

region = st.sidebar.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())
category = st.sidebar.multiselect("Category", df["Category"].unique(), default=df["Category"].unique())

filtered_df = df[(df["Region"].isin(region)) & (df["Category"].isin(category))]

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["OrderID"].nunique()

st.metric("Total Sales", total_sales)
st.metric("Total Profit", total_profit)
st.metric("Total Orders", total_orders)

trend = filtered_df.groupby("OrderDate")["Sales"].sum().reset_index()
fig = px.line(trend, x="OrderDate", y="Sales")
st.plotly_chart(fig)
