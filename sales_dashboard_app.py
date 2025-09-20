# sales_dashboard_app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Analysis Dashboard", layout="wide")
st.title("📊 Sales Analysis Dashboard")

# -----------------------------
# Step 1: Generate Sample Data
# -----------------------------
np.random.seed(42)
num_records = 500

sample_data = {
    "OrderID": range(1, num_records + 1),
    "Date": pd.date_range(start="2023-01-01", periods=num_records, freq='D'),
    "Product": np.random.choice(
        ["Laptop", "Smartphone", "Headphones", "Camera", "Monitor", "Keyboard"], num_records),
    "Category": np.random.choice(
        ["Electronics", "Accessories"], num_records),
    "Quantity": np.random.randint(1, 10, num_records),
    "Price": np.random.randint(50, 1000, num_records),
    "Region": np.random.choice(["North", "South", "East", "West"], num_records)
}

df = pd.DataFrame(sample_data)

# -----------------------------
# Step 2: Data Cleaning & Prep
# -----------------------------
df['Date'] = pd.to_datetime(df['Date'])
df['TotalRevenue'] = df['Quantity'] * df['Price']
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year
df['MonthYear'] = df['Date'].dt.to_period('M')  # Keep as Period initially

# -----------------------------
# Step 3: Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")
selected_region = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())
selected_category = st.sidebar.multiselect("Select Category", df['Category'].unique(), default=df['Category'].unique())

filtered_df = df[(df['Region'].isin(selected_region)) & (df['Category'].isin(selected_category))]

# -----------------------------
# Step 4: KPIs
# -----------------------------
total_revenue = filtered_df['TotalRevenue'].sum()
total_orders = filtered_df['OrderID'].nunique()
average_order_value = filtered_df['TotalRevenue'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("🛒 Average Order Value", f"${average_order_value:,.2f}")

# -----------------------------
# Step 5: Monthly Revenue Trend
# -----------------------------
monthly_sales = filtered_df.groupby('MonthYear')['TotalRevenue'].sum().reset_index()

# ✅ Convert MonthYear to datetime to avoid Seaborn TypeError
monthly_sales['MonthYear'] = monthly_sales['MonthYear'].apply(lambda x: x.start_time if hasattr(x, 'start_time') else pd.to_datetime(x))
monthly_sales['TotalRevenue'] = pd.to_numeric(monthly_sales['TotalRevenue'], errors='coerce')
monthly_sales = monthly_sales.dropna(subset=['MonthYear', 'TotalRevenue'])

plt.figure(figsize=(10,5))
plt.plot(monthly_sales['MonthYear'], monthly_sales['TotalRevenue'], marker='o', color='blue')
plt.title("Monthly Revenue Trend")
plt.xticks(rotation=45)
plt.ylabel("Revenue")
plt.xlabel("Month-Year")
st.pyplot(plt.gcf())
plt.clf()

# -----------------------------
# Step 6: Top Products
# -----------------------------
top_products = filtered_df.groupby('Product')['TotalRevenue'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(8,5))
sns.barplot(x=top_products.values, y=top_products.index, palette='viridis')
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
st.pyplot(plt.gcf())
plt.clf()

# -----------------------------
# Step 7: Revenue by Region
# -----------------------------
region_sales = filtered_df.groupby('Region')['TotalRevenue'].sum().sort_values(ascending=False)

plt.figure(figsize=(6,4))
sns.barplot(x=region_sales.values, y=region_sales.index, palette='coolwarm')
plt.title("Revenue by Region")
plt.xlabel("Revenue")
plt.ylabel("Region")
st.pyplot(plt.gcf())
plt.clf()

# -----------------------------
# Step 8: Raw Data Table
# -----------------------------
st.subheader("Raw Data")
st.dataframe(filtered_df)

