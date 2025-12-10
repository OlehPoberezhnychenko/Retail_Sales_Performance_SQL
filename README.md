# 🇧🇷 Olist E-Commerce Analysis

![SQL](https://img.shields.io/badge/Language-SQL-orange) ![Python](https://img.shields.io/badge/Python-Integration-blue)

## 📊 Project Overview
This project analyzes **100,000+ real e-commerce orders** from the Olist Store in Brazil.
* **Goal:** Optimize logistics and identify top-performing product categories.
* **Tech Stack:** Advanced SQL (Window Functions, Joins) and Python for visualization.
* **Data Source:** [Brazilian E-Commerce Public Dataset (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## 🔍 Key Insights
1.  **Category Dominance:** "Bed, Bath, Table" and "Health/Beauty" are the primary revenue drivers.
2.  **Logistics:** Delivery times vary significantly by state, with remote regions experiencing delays up to **40% higher** than the average.

## 📉 Visual Analysis

### 1. Order Status Distribution
*The vast majority of orders are successfully delivered, but there is a visible segment of shipped/canceled orders.*
![Status](images/01_order_status.png)

### 2. Top Product Categories
*Visualizing the top 10 categories by sales volume.*
![Categories](images/02_top_categories.png)

## 💻 SQL Query Example
*Calculating average delivery time by state:*
```sql
SELECT 
    customer_state,
    AVG(order_delivered_date - purchase_timestamp) as avg_delivery_days
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY 1;
