# =====================================================
# IMPORTS
# =====================================================
import pandas as pd
from db_connection import get_connection


# =====================================================
# GENERIC TABLE LOADER (REUSABLE FUNCTION)
# =====================================================
def load_table(table_name, source_name):
    """
    Load any table safely and add Source column
    """

    conn = get_connection()

    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

        # Remove extra spaces in column names
        df.columns = df.columns.str.strip()

        # Add business source
        df["Source"] = source_name

        # Ensure Date column exists
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    except Exception as e:
        print(f"⚠️ Could not load table '{table_name}': {e}")
        df = pd.DataFrame()

    conn.close()
    return df


# =====================================================
# LOAD INDIVIDUAL DATASETS
# =====================================================
def get_sales_data():
    return load_table("sales", "Sales")


def get_retail_data():
    return load_table("retail_sales", "Retail")


def get_wholesale_data():
    return load_table("wholesale_sales", "Wholesale")


def get_ecommerce_data():
    return load_table("ecommerce_sales", "Ecommerce")


# =====================================================
# COMBINED DATASET (MAIN DASHBOARD DATA)
# =====================================================
def get_all_data():

    sales = get_sales_data()
    retail = get_retail_data()
    ecommerce = get_ecommerce_data()
    wholesale = get_wholesale_data()

    df = pd.concat(
        [sales, retail, ecommerce, wholesale],
        ignore_index=True
    )

    return df


# =====================================================
# KPI — TOTAL SALES (ALL SOURCES)
# =====================================================
def total_sales():
    df = get_all_data()

    if "Sales" in df.columns:
        return df["Sales"].sum()

    return 0


# =====================================================
# SALES BY CATEGORY (ALL SOURCES)
# =====================================================
def sales_by_category():
    df = get_all_data()

    if "Category" not in df.columns:
        return pd.DataFrame()

    result = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index(name="total")
    )

    return result