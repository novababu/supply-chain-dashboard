import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("supply_chain_data.csv")

df = load_data()

st.title("📦 Supply Chain Management Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
product_filter = st.sidebar.multiselect("Select Product Type", options=df["Product Type"].unique(), default=df["Product Type"].unique())
filtered_df = df[df["Product Type"].isin(product_filter)]

# --- Inventory Management ---
st.header("🗃️ Inventory Management")
inventory_chart = px.bar(filtered_df, x="SKU", y="Stock levels", color="Product Type", title="Inventory by SKU")
st.plotly_chart(inventory_chart, use_container_width=True)

# --- Order Fulfillment ---
st.header("📦 Order Fulfillment")
if "FulfillmentStatus" in df.columns:
    fulfillment_status = df["FulfillmentStatus"].value_counts().reset_index()
    fulfillment_chart = px.pie(fulfillment_status, values="FulfillmentStatus", names="index", title="Order Fulfillment Status")
    st.plotly_chart(fulfillment_chart, use_container_width=True)

# --- Supplier Performance ---
st.header("🏭 Supplier Performance")
supplier_chart = px.bar(filtered_df, x="Supplier name", y="Defect rates", color="Supplier name", title="Defect Rate by Supplier")
st.plotly_chart(supplier_chart, use_container_width=True)

# --- Transportation Efficiency ---
st.header("🚚 Transportation Efficiency")
if "Carrier" in df.columns and "TransitTime" in df.columns:
    transit_chart = px.scatter(filtered_df, x="Carrier", y="TransitTime", color="DeliveryStatus", title="Transit Time by Carrier")
    st.plotly_chart(transit_chart, use_container_width=True)

# --- Supply Chain Costs ---
st.header("💰 Supply Chain Costs")
if "CostType" in df.columns:
    cost_data = df.groupby("CostType")["Shipping costs"].sum().reset_index()
    cost_chart = px.pie(cost_data, names="CostType", values="Shipping costs", title="Cost Distribution")
    st.plotly_chart(cost_chart, use_container_width=True)

st.markdown("📊 All visualizations are interactive. Use filters on the sidebar to customize your view.")

