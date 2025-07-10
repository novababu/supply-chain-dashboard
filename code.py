import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("supply_chain_data.csv")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

if "product_type" in df.columns:
    product_filter = st.sidebar.multiselect(
        "Select Product Type", 
        options=df["product_type"].dropna().unique(), 
        default=df["product_type"].dropna().unique()
    )
    df = df[df["product_type"].isin(product_filter)]

st.title("📦 Supply Chain Management Dashboard")

# --- Inventory Management ---
st.header("🗃️ Inventory Management")
if "sku" in df.columns and "stock_levels" in df.columns:
    inventory_chart = px.bar(df, x="sku", y="stock_levels", color="product_type", title="Inventory by SKU")
    st.plotly_chart(inventory_chart, use_container_width=True)

# --- Order Fulfillment ---
st.header("📦 Order Fulfillment")
if "fulfillmentstatus" in df.columns:
    fulfillment_data = df["fulfillmentstatus"].value_counts().reset_index()
    fulfillment_data.columns = ["status", "count"]
    fulfillment_chart = px.pie(fulfillment_data, values="count", names="status", title="Order Fulfillment Status")
    st.plotly_chart(fulfillment_chart, use_container_width=True)

# --- Supplier Performance ---
st.header("🏭 Supplier Performance")
if "supplier_name" in df.columns and "defect_rates" in df.columns:
    supplier_chart = px.bar(df, x="supplier_name", y="defect_rates", color="supplier_name", title="Defect Rate by Supplier")
    st.plotly_chart(supplier_chart, use_container_width=True)

# --- Transportation Efficiency ---
st.header("🚚 Transportation Efficiency")
if "carrier" in df.columns and "transittime" in df.columns and "deliverystatus" in df.columns:
    transit_chart = px.scatter(df, x="carrier", y="transittime", color="deliverystatus", title="Transit Time by Carrier")
    st.plotly_chart(transit_chart, use_container_width=True)

# --- Supply Chain Costs ---
st.header("💰 Supply Chain Costs")
if "costtype" in df.columns and "shipping_costs" in df.columns:
    cost_data = df.groupby("costtype")["shipping_costs"].sum().reset_index()
    cost_chart = px.pie(cost_data, names="costtype", values="shipping_costs", title="Cost Distribution")
    st.plotly_chart(cost_chart, use_container_width=True)

st.markdown("---")
st.markdown("ℹ️ Use the filters on the left to interact with the dashboard and drill down into specific product types.")


