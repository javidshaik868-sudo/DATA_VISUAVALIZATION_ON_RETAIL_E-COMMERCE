import sqlite3
import pandas as pd
import os

os.makedirs("database", exist_ok=True)

df = pd.read_csv("data/sales_data.csv")

conn = sqlite3.connect("database/project.db")

df.to_sql("sales", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Database created successfully")