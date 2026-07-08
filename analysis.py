import sqlite3
import pandas as pd

# ================================================
# Olist E-Commerce Portfolio Project
# Analyst: Azeem Malik
# Dataset: Brazilian E-Commerce (Olist) — Kaggle
# Questions: 5 business questions answered with SQL
# ================================================

conn = sqlite3.connect('olist_portfolio.db')

# ================================================
# QUESTION 1 — Monthly Revenue Trend
# Business question: How did revenue trend 
# month by month across the whole dataset?
# ================================================
q1 = """
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

# ================================================
# QUESTION 2 — Top 10 Customers By Spend
# Business question: Who are our highest 
# spending customers?
# ================================================
q2 = """
SELECT
    orders.customer_id,
    ROUND(SUM(order_items.price), 2) AS total_spent
FROM orders
JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY orders.customer_id
ORDER BY total_spent DESC
LIMIT 10;
"""

# ================================================
# QUESTION 3 — Best Performing Categories
# Business question: Which product categories 
# generate the most revenue?
# ================================================
q3 = """
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

# ================================================
# QUESTION 4 — Delivery Performance
# Business question: How many orders were 
# delivered on time versus late?
# ================================================
q4 = """
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

# ================================================
# QUESTION 5 — Average Order Value By Month
# Business question: What was the average 
# order value each month?
# ================================================
q5 = """
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

# ================================================
# RUN ALL QUESTIONS AND PRINT RESULTS
# ================================================
questions = [
    ("Question 1 — Monthly Revenue Trend", q1),
    ("Question 2 — Top 10 Customers By Spend", q2),
    ("Question 3 — Best Performing Categories", q3),
    ("Question 4 — Delivery Performance", q4),
    ("Question 5 — Average Order Value By Month", q5),
]

for title, query in questions:
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

conn.close()
input("\nPress Enter to exit...")