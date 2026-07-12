import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ================================================
# Setup
# ================================================
conn = sqlite3.connect('olist_portfolio.db')

# Set the visual style
sns.set_theme(style='darkgrid')

# ================================================
# CHART 1 — Monthly Revenue Trend
# ================================================

# Pull the data using our Question 1 query
query = """
SELECT
    strftime('%Y-%m', 
        substr(orders.order_purchase_timestamp, 7, 4) 
        || '-' || 
        substr(orders.order_purchase_timestamp, 4, 2) 
        || '-' || 
        substr(orders.order_purchase_timestamp, 1, 2)
    ) AS month,
    ROUND(SUM(order_items.price), 2) AS total_revenue
FROM orders
JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY month
ORDER BY month ASC;
"""

df = pd.read_sql_query(query, conn)

# Remove incomplete months at start and end
df = df[df['month'] >= '2017-01']
df = df[df['month'] <= '2018-08']

# Create the chart
plt.figure(figsize=(14, 6))

sns.lineplot(
    data=df,
    x='month',
    y='total_revenue',
    color='#2ecc71',
    linewidth=2.5,
    marker='o'
)

# Add labels and title
plt.title('Monthly Revenue Trend — Olist E-Commerce',
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Revenue (R$)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the chart
plt.savefig('chart1_monthly_revenue.png', dpi=150)
print("Chart 1 saved successfully.")

conn.close()

# ================================================
# CHART 2 — Top 10 Customers By Spend
# ================================================

conn = sqlite3.connect('olist_portfolio.db')

query2 = """
SELECT
    SUBSTR(orders.customer_id, 1, 8) AS customer,
    ROUND(SUM(order_items.price), 2) AS total_spent
FROM orders
JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY orders.customer_id
ORDER BY total_spent DESC
LIMIT 10;
"""

df2 = pd.read_sql_query(query2, conn)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=df2,
    x='customer',
    y='total_spent',
    color='#3498db'
)

plt.title('Top 10 Customers By Total Spend',
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Customer ID (shortened)', fontsize=12)
plt.ylabel('Total Spent (R$)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('chart2_top_customers.png', dpi=150)
print("Chart 2 saved successfully.")

# ================================================
# CHART 3 — Best Performing Categories
# ================================================

query3 = """
SELECT
    category_translation.product_category_name_english,
    ROUND(SUM(order_items.price), 2) AS total_revenue
FROM order_items
JOIN products ON order_items.product_id = products.product_id
JOIN category_translation 
    ON products.product_category_name = 
       category_translation.product_category_name
GROUP BY category_translation.product_category_name_english
ORDER BY total_revenue DESC
LIMIT 10;
"""

df3 = pd.read_sql_query(query3, conn)

plt.figure(figsize=(12, 6))

sns.barplot(
    data=df3,
    x='total_revenue',
    y='product_category_name_english',
    color='#e74c3c'
)

plt.title('Top 10 Product Categories By Revenue',
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Total Revenue (R$)', fontsize=12)
plt.ylabel('Category', fontsize=12)
plt.tight_layout()

plt.savefig('chart3_top_categories.png', dpi=150)
print("Chart 3 saved successfully.")

# ================================================
# CHART 4 — Delivery Performance
# ================================================

query4 = """
SELECT
    CASE WHEN order_delivered_customer_date <= 
              order_estimated_delivery_date
         THEN 'On Time'
         ELSE 'Late'
    END AS delivery_status,
    COUNT(order_id) AS total_orders
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
GROUP BY delivery_status
ORDER BY total_orders DESC;
"""

df4 = pd.read_sql_query(query4, conn)

plt.figure(figsize=(8, 6))

colors = ['#2ecc71', '#e74c3c']
plt.pie(
    df4['total_orders'],
    labels=df4['delivery_status'],
    colors=colors,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 13}
)

plt.title('Order Delivery Performance',
          fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()

plt.savefig('chart4_delivery_performance.png', dpi=150)
print("Chart 4 saved successfully.")

# ================================================
# CHART 5 — Average Order Value By Month
# ================================================

query5 = """
SELECT
    strftime('%Y-%m', 
        substr(orders.order_purchase_timestamp, 7, 4) 
        || '-' || 
        substr(orders.order_purchase_timestamp, 4, 2) 
        || '-' || 
        substr(orders.order_purchase_timestamp, 1, 2)
    ) AS month,
    ROUND(AVG(order_items.price), 2) AS avg_order_value
FROM orders
JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY month
ORDER BY month ASC;
"""

df5 = pd.read_sql_query(query5, conn)

df5 = df5[df5['month'] >= '2017-01']
df5 = df5[df5['month'] <= '2018-08']

plt.figure(figsize=(14, 6))

sns.lineplot(
    data=df5,
    x='month',
    y='avg_order_value',
    color='#9b59b6',
    linewidth=2.5,
    marker='o'
)

plt.title('Average Order Value By Month',
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Average Order Value (R$)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('chart5_avg_order_value.png', dpi=150)
print("Chart 5 saved successfully.")

conn.close()
print("\nAll charts saved successfully!")