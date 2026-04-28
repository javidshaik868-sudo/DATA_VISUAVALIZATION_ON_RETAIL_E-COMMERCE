# =====================================================
# IMPORTS
# =====================================================
import streamlit as st
import backend as bk
import matplotlib.pyplot as plt
import pandas as pd

# =====================================================
# CUSTOM BACKGROUND FUNCTION
# =====================================================
def set_bg(color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# PAGE SETTINGS
# =====================================================
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 SHAIK SHARES ")

# =====================================================
# LOAD DATA
# =====================================================
df = bk.get_all_data()

# ---------------- SAFETY FIXES ----------------
# Standardize column names
df.columns = df.columns.str.strip()

# Ensure Source column exists
if "Source" not in df.columns:
    df["Source"] = "Sales"

# Convert Date column safely
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Debug (optional)
st.write("Columns:", df.columns)
st.dataframe(df.head())

# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.header("🎛 Dashboard Controls")

# Source Filter
source_filter = st.sidebar.multiselect(
    "Select Business Type",
    df["Source"].unique(),
    default=df["Source"].unique()
)

# Category Filter
category_filter = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

# Chart Selector
chart_option = st.sidebar.selectbox(
    "Select Visualization",
    ["Bar Chart", "Line Chart", "Histogram",
     "Scatter Plot", "Pie Chart"]
)

# Apply Filters
filtered_df = df[
    (df["Source"].isin(source_filter)) &
    (df["Category"].isin(category_filter))
]

# =====================================================
# KPI SECTION
# =====================================================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

total_sales = filtered_df["Sales"].sum()
avg_sales = filtered_df["Sales"].mean()
total_products = filtered_df["Product"].nunique()

col1.metric("💰 Total Sales", f"{total_sales:,.0f}")
col2.metric("📈 Avg Sales", f"{avg_sales:,.0f}")
col3.metric("🛒 Products", total_products)

# =====================================================
# TABS LAYOUT
# =====================================================
tab1, tab2, tab3 = st.tabs(
    ["📊 Charts", "📈 Insights", "🗂 Dataset"]
)

# =====================================================
# TAB 1 — CHARTS (BLUE BACKGROUND)
# =====================================================
with tab1:

    set_bg("#E3F2FD")   # Light Blue

    st.subheader("Charts Dashboard")

    if chart_option == "Bar Chart":
        st.subheader("Top Products")

        top_products = (
            filtered_df.groupby("Product")["Sales"]
            .sum()
            .nlargest(10)
        )

        fig, ax = plt.subplots()
        top_products.plot(kind="bar", ax=ax)
        st.pyplot(fig)

    elif chart_option == "Histogram":
        st.subheader("Sales Distribution")

        fig, ax = plt.subplots()
        ax.hist(filtered_df["Sales"], bins=30)
        st.pyplot(fig)

    elif chart_option == "Scatter Plot":
        st.subheader("Profit vs Sales")

        fig, ax = plt.subplots()
        ax.scatter(filtered_df["Sales"], filtered_df["Profit"])
        st.pyplot(fig)

    elif chart_option == "Pie Chart":
        st.subheader("Category Share")

        category_data = (
            filtered_df.groupby("Category")["Sales"].sum()
        )

        fig, ax = plt.subplots()
        ax.pie(category_data, labels=category_data.index,
               autopct="%1.1f%%")
        st.pyplot(fig)

# =====================================================
# TAB 2 — INSIGHTS (GREEN BACKGROUND)
# =====================================================
with tab2:

    set_bg("#E8F5E9")   # Light Green

    st.subheader("Business Insights")

    comparison = filtered_df.groupby("Source")["Sales"].sum()

    fig, ax = plt.subplots()
    comparison.plot(kind="bar", ax=ax)
    st.pyplot(fig)

# =====================================================
# TAB 3 — DATASET (LIGHT ORANGE BACKGROUND)
# =====================================================
with tab3:

    set_bg("#FFF3E0")   # Light Orange

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df)