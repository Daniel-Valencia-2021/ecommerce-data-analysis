import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="E-commerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_pickle("data/processed/clean_data.pkl")

df = load_data()

# ---------------- PREPROCESS ----------------
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Filtros")

country = st.sidebar.selectbox("🌍 País", df["Country"].unique())

df = df[df["Country"] == country]

# ---------------- KPIs ----------------
total_sales = df["TotalPrice"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()

st.title("📊 Dashboard E-commerce")
st.markdown("Análisis de ventas y comportamiento del negocio")

st.markdown("## 📌 Indicadores clave")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Ventas Totales", f"${total_sales:,.0f}")
col2.metric("📦 Órdenes", f"{total_orders:,}")
col3.metric("👤 Clientes", f"{total_customers:,}")

st.divider()

# ---------------- GRÁFICAS ----------------

# 📈 Ventas por mes
sales_by_month = df.groupby("YearMonth")["TotalPrice"].sum()

fig1, ax1 = plt.subplots()
sales_by_month.plot(ax=ax1, marker="o")
ax1.set_title("📈 Ventas por mes")
ax1.set_xlabel("Mes")
ax1.set_ylabel("Ventas")

# 🛍️ Top productos
top_products = (
    df.groupby("Description")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig2, ax2 = plt.subplots()
top_products.sort_values().plot(kind="barh", ax=ax2)
ax2.set_title("🛍️ Top 10 productos")

# 🌍 Ventas por país
sales_by_country = (
    df.groupby("Country")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig3, ax3 = plt.subplots()
sales_by_country.plot(kind="bar", ax=ax3)
ax3.set_title("🌍 Ventas por país")

# 👤 Top clientes
top_customers = (
    df.groupby("CustomerID")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig4, ax4 = plt.subplots()
top_customers.plot(kind="bar", ax=ax4)
ax4.set_title("👤 Top clientes")

# ---------------- LAYOUT ----------------

col1, col2 = st.columns(2)

with col1:
    st.pyplot(fig1)

with col2:
    st.pyplot(fig3)

col3, col4 = st.columns(2)

with col3:
    st.pyplot(fig2)

with col4:
    st.pyplot(fig4)

st.divider()

# ---------------- INSIGHTS ----------------

st.markdown("## 💡 Insights de negocio")

st.info(
    "📈 Las ventas presentan un crecimiento significativo en el último trimestre del año, "
    "especialmente en noviembre, lo que indica una fuerte estacionalidad."
)

st.info(
    "🛍️ Un grupo reducido de productos concentra la mayor parte de los ingresos, "
    "lo que puede representar una dependencia del negocio en estos artículos."
)

st.info(
    "👤 Un pequeño grupo de clientes genera la mayoría de las ventas, evidenciando un comportamiento tipo Pareto."
)

st.info(
    "🌍 Las ventas están concentradas en ciertos países, lo que sugiere oportunidades de expansión."
)