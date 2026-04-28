import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Create data folder if not exists
os.makedirs("data", exist_ok=True)

# -----------------------------
# COMMON DATA
# -----------------------------
categories = ["Electronics", "Fashion", "Furniture", "Grocery", "Sports"]

products = {
    "Electronics": ["Laptop", "Mobile", "Headphones", "Tablet", "Camera"],
    "Fashion": ["T-Shirt", "Jeans", "Shoes", "Jacket", "Watch"],
    "Furniture": ["Chair", "Table", "Sofa", "Bed", "Cupboard"],
    "Grocery": ["Rice", "Oil", "Milk", "Snacks", "Sugar"],
    "Sports": ["Cricket Bat", "Football", "Tennis Racket", "Gloves", "Helmet"]
}

start_date = datetime(2023, 1, 1)


# -----------------------------
# FUNCTION TO GENERATE DATA
# -----------------------------
def generate_sales_data(rows, business_type):
    data = []

    for _ in range(rows):
        category = random.choice(categories)
        product = random.choice(products[category])

        date = start_date + timedelta(days=random.randint(0, 730))

        # Different sales ranges
        if business_type == "ecommerce":
            sales = random.randint(500, 15000)
        else:  # wholesale
            sales = random.randint(10000, 90000)

        data.append([
            date.strftime("%Y-%m-%d"),
            category,
            product,
            sales
        ])

    df = pd.DataFrame(
        data,
        columns=["Date", "Category", "Product", "Sales"]
    )

    return df


# -----------------------------
# GENERATE 1500 ROWS EACH
# -----------------------------
ecommerce_df = generate_sales_data(1500, "ecommerce")
wholesale_df = generate_sales_data(1500, "wholesale")

# Save CSV files
ecommerce_df.to_csv("data/ecommerce_sales.csv", index=False)
wholesale_df.to_csv("data/wholesale_sales.csv", index=False)

print("✅ 1500 rows created for Ecommerce & Wholesale datasets!")