import pandas as pd
import sqlite3
import os

# =====================================================
# DATABASE CONNECTION
# =====================================================
DB_PATH = "database/project.db"

# CSV files and corresponding table names
FILES = {
    "data/retail_sales.csv": "retail_sales",
    "data/wholesale_sales.csv": "wholesale_sales"
}


def load_csv_to_database():
    """Load CSV files into SQLite database tables"""

    # Connect to database
    conn = sqlite3.connect(DB_PATH)

    try:
        for file_path, table_name in FILES.items():

            if os.path.exists(file_path):
                print(f"📂 Loading {file_path}...")

                # Read CSV
                df = pd.read_csv(file_path)

                # Insert into database
                df.to_sql(
                    table_name,
                    conn,
                    if_exists="replace",   # change to 'append' if needed
                    index=False
                )

                print(f"✅ Table '{table_name}' created successfully")

            else:
                print(f"❌ File not found: {file_path}")

        print("\n🎉 All data imported into project.db successfully!")

    finally:
        conn.close()


# =====================================================
# RUN SCRIPT
# =====================================================
if __name__ == "__main__":
    load_csv_to_database()