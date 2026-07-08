import sqlite3
import pandas as pd

# Connect to (or create) the database file
conn = sqlite3.connect('olist_portfolio.db')

# Load each CSV into the database as a table
print("Loading orders...")
pd.read_csv('olist_orders_dataset.csv').to_sql(
    'orders', conn, if_exists='replace', index=False)

print("Loading order items...")
pd.read_csv('olist_order_items_dataset.csv').to_sql(
    'order_items', conn, if_exists='replace', index=False)

print("Loading products...")
pd.read_csv('olist_products_dataset.csv').to_sql(
    'products', conn, if_exists='replace', index=False)

print("Loading category translations...")
pd.read_csv('product_category_name_translation.csv').to_sql(
    'category_translation', conn, if_exists='replace', index=False)

print("Done! Database created successfully.")
conn.close()