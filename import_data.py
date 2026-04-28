# =====================================================
# IMPORTS
# =====================================================
import pandas as pd
import sqlite3
import os

# =====================================================
# DATABASE CONNECTION
# =====================================================
db_path = "database/project.db"

# create database folder if not exists
os.makedirs("database", exist_ok=True)

conn = sqlite3.connect(db_path)

print("✅ Connected to database")

# =====================================================
# CSV FILES TO IMPORT
# =====================================================
files = {
    "data/retail_sales.csv": "retail_sales",
    "data/wholesale_sales.csv": "wholesale_sales"
}

# =====================================================
# IMPORT CSV → SQLITE
# =====================================================
for file_path, table_name in files.items():

    if os.path.exists(file_path):

        print(f"📂 Loading {file_path}...")

        df = pd.read_csv(file_path)

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",   # replace old table
            index=False
        )

        print(f"✅ Table '{table_name}' imported successfully")

    else:
        print(f"❌ File NOT FOUND: {file_path}")

# =====================================================
# CLOSE CONNECTION
# =====================================================
conn.close()

print("\n🎉 ALL DATA IMPORTED INTO project.db")