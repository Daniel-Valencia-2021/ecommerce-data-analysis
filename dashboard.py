import streamlit as st
import pandas as pd

# Configuración
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# Título
st.title("📊 Dashboard E-commerce")
st.markdown("Análisis de ventas y comportamiento del negocio")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_pickle("data/processed/clean_data.pkl")

df = load_data()

# Crear variables
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

# KPIs
total_sales = df["TotalPrice"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Ventas Totales", f"${total_sales:,.0f}")
col2.metric("📦 Órdenes", total_orders)
col3.metric("👤 Clientes", total_customers)

st.divider()

# 📈 Ventas por mes
st.subheader("📈 Ventas por mes")

sales_by_month = df.groupby("YearMonth")["TotalPrice"].sum()

st.line_chart(sales_by_month)

# 🛍️ Top productos
st.subheader("🛍️ Top 10 productos")

top_products = df.groupby("Description")["TotalPrice"].sum().sort_values(ascending=False).head(10)

st.bar_chart(top_products)

# 🌍 Ventas por país
st.subheader("🌍 Ventas por país")

sales_by_country = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).head(10)

st.bar_chart(sales_by_country)

# 👤 Top clientes
st.subheader("👤 Top clientes")

top_customers = df.groupby("CustomerID")["TotalPrice"].sum().sort_values(ascending=False).head(10)

st.bar_chart(top_customers)