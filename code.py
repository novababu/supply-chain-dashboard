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

# Dynamic filtering
if "product_type" in df.columns:
    df = df[df["product_type"].isin(
        st.sidebar.multiselect("Product Type", df["product_type"].dropna().unique(), default=df["product_type"].dropna().unique())
    )]

if "availability" in df.columns:
    df = df[df["availability"].isin(
        st.sidebar.multiselect("Availability", df["availability"].dropna().unique(), default=df["availability"].dropna().unique())
    )]

if "location" in df.columns:
    df = df[df["location"].isin(
        st.sidebar.multiselect("Location", df["location"].dropna().unique(), default=df["location"].dropna().unique())
    )]

if "supplier_name" in df.columns:
    df = df[df["supplier_name"].isin(
        st.sidebar.multiselect("Supplier", df["supplier_name"].dropna().unique(), default=df["supplier_name"].dropna().unique())
    )]

st.title("📦 Enhanced Supply Chain Management Dashboard")

# --- Inventory Management ---
st.header("🗃️ Inventory Management")
if "sku" in df.columns and "stock_levels" in df.columns:
    st.subheader("Inventory Levels by SKU")
    st.plotly_chart(px.bar(df, x="sku", y="stock_levels", color="product_type", title="Inventory by SKU"), use_container_width=True)

# --- Order Fulfillment ---
st.header("📦 Order Fulfillment")
if "fulfillmentstatus" in df.columns:
    st.subheader("Fulfillment Status")
    status_counts = df["fulfillmentstatus"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]
    st.plotly_chart(px.pie(status_counts, names="status", values="count", title="Fulfillment Breakdown"), use_container_width=True)

# --- Supplier Performance ---
st.header("🏭 Supplier Performance")
if "defect_rates" in df.columns:
    st.subheader("Defect Rates by Supplier")
    st.plotly_chart(px.bar(df, x="supplier_name", y="defect_rates", color="supplier_name", title="Defect Rate"), use_container_width=True)

# --- Transportation Efficiency ---
st.header("🚚 Transportation Efficiency")
if "carrier" in df.columns and "transittime" in df.columns and "deliverystatus" in df.columns:
    st.subheader("Transit Time vs Delivery Status")
    st.plotly_chart(px.scatter(df, x="carrier", y="transittime", color="deliverystatus", title="Carrier Transit Time"), use_container_width=True)

# --- Supply Chain Costs ---
st.header("💰 Cost Analysis")
if "costtype" in df.columns and "shipping_costs" in df.columns:
    st.subheader("Cost Distribution")
    cost_data = df.groupby("costtype")["shipping_costs"].sum().reset_index()
    st.plotly_chart(px.pie(cost_data, names="costtype", values="shipping_costs", title="Cost Breakdown"), use_container_width=True)

# --- Top-Selling Products ---
st.header("🔥 Top-Selling Products")
if "number_of_products_sold" in df.columns:
    top_sellers = df.groupby("product_type")["number_of_products_sold"].sum().reset_index().sort_values(by="number_of_products_sold", ascending=False)
    st.plotly_chart(px.bar(top_sellers, x="product_type", y="number_of_products_sold", color="product_type", title="Top Products Sold"), use_container_width=True)

# --- Revenue Analysis ---
st.header("💵 Revenue Analysis")
if "revenue_generated" in df.columns and "product_type" in df.columns:
    revenue_data = df.groupby("product_type")["revenue_generated"].sum().reset_index()
    st.plotly_chart(px.bar(revenue_data, x="product_type", y="revenue_generated", color="product_type", title="Revenue by Product Type"), use_container_width=True)

# --- Lead Time Trends ---
st.header("⏱️ Lead Time Trends")
if "lead_time" in df.columns:
    st.subheader("Average Lead Time by Supplier")
    lead_data = df.groupby("supplier_name")["lead_time"].mean().reset_index()
    st.plotly_chart(px.bar(lead_data, x="supplier_name", y="lead_time", color="supplier_name", title="Avg Lead Time"), use_container_width=True)

# --- Inspection Trends ---
st.header("🔍 Inspection Results")
if "inspection_results" in df.columns:
    inspection = df["inspection_results"].value_counts().reset_index()
    inspection.columns = ["result", "count"]
    st.plotly_chart(px.pie(inspection, names="result", values="count", title="Inspection Outcome"), use_container_width=True)

# --- Shipping Mode Analysis ---
st.header("🚢 Shipping Mode Analysis")
if "transportation_modes" in df.columns and "routes" in df.columns:
    st.subheader("Shipping Mode vs Routes")
    route_data = df.groupby("transportation_modes")["routes"].count().reset_index()
    route_data.columns = ["mode", "routes"]
    st.plotly_chart(px.bar(route_data, x="mode", y="routes", color="mode", title="Shipping Modes by Route Count"), use_container_width=True)

st.markdown("—")
st.markdown("🔍 Use sidebar filters to customize your analysis.")



