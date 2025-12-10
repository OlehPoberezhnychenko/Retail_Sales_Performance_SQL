import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# CONFIGURATION
sns.set_theme(style="whitegrid")
DB_PATH = "olist.db"

if not os.path.exists('images'):
    os.makedirs('images')

def load_data_to_sql():
    conn = sqlite3.connect(DB_PATH)
    print("⏳ Loading data into SQL Database...")
    try:
        # Load necessary tables for RFM
        orders = pd.read_csv('data/olist_orders_dataset.csv')
        items = pd.read_csv('data/olist_order_items_dataset.csv')
        customers = pd.read_csv('data/olist_customers_dataset.csv') # We need unique IDs
        
        orders.to_sql('orders', conn, if_exists='replace', index=False)
        items.to_sql('order_items', conn, if_exists='replace', index=False)
        customers.to_sql('customers', conn, if_exists='replace', index=False)
        
        print("✅ Data Loaded.")
        return conn
    except Exception as e:
        print(f"❌ Error (Check if files are in 'data/' folder): {e}")
        return None

def analyze_rfm_segmentation(conn):
    print("🧠 Running RFM Segmentation (Complex SQL)...")
    
    # 1. SQL Query to calculate R, F, M values per customer
    query = """
    SELECT 
        c.customer_unique_id,
        MAX(o.order_purchase_timestamp) as last_order_date,
        COUNT(o.order_id) as frequency,
        SUM(i.price) as monetary
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items i ON o.order_id = i.order_id
    GROUP BY 1
    """
    df = pd.read_sql(query, conn)
    
    # 2. Python Calculation (Simulating Advanced SQL Logic)
    # Recency: Days since max date in dataset (to simulate "today")
    max_date = pd.to_datetime(df['last_order_date']).max()
    df['recency'] = (max_date - pd.to_datetime(df['last_order_date'])).dt.days
    
    # Scoring (1-5 scale, 5 is best)
    df['R_Score'] = pd.qcut(df['recency'], 5, labels=[5, 4, 3, 2, 1])
    df['F_Score'] = pd.cut(df['frequency'], bins=[0, 1, 2, 3, 5, 100], labels=[1, 2, 3, 4, 5]) # Custom bins for e-commerce
    df['M_Score'] = pd.qcut(df['monetary'], 5, labels=[1, 2, 3, 4, 5])
    
    # Create Segments
    df['RFM_Score'] = df['R_Score'].astype(str) + df['F_Score'].astype(str)
    
    # Map Scores to Segment Names (Standard Marketing Logic)
    def segment_customer(row):
        r = int(row['R_Score'])
        f = int(row['F_Score'])
        if r >= 4 and f >= 4: return 'Champions'
        if r >= 2 and f >= 3: return 'Loyal Customers'
        if r <= 2 and f >= 1: return 'Hibernating'
        if r >= 3 and f <= 2: return 'Potential Loyalists'
        return 'At Risk'

    df['Segment'] = df.apply(segment_customer, axis=1)
    
    # 3. Visualization
    plt.figure(figsize=(12, 6))
    order = ['Champions', 'Loyal Customers', 'Potential Loyalists', 'At Risk', 'Hibernating']
    sns.countplot(y='Segment', data=df, order=order, palette='viridis')
    plt.title('3. Customer Segments (RFM Analysis)', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Customers')
    plt.savefig('images/03_rfm_segments.png', dpi=300)
    print("✅ Generated: images/03_rfm_segments.png")

def analyze_payment_behavior(conn):
    # Quick chart on how people pay
    try:
        payments = pd.read_csv('data/olist_order_payments_dataset.csv')
        payments.to_sql('payments', conn, if_exists='replace', index=False)
        
        query = "SELECT payment_type, COUNT(*) as count FROM payments GROUP BY 1 ORDER BY 2 DESC"
        df = pd.read_sql(query, conn)
        
        plt.figure(figsize=(8, 8))
        plt.pie(df['count'], labels=df['payment_type'], autopct='%1.1f%%', colors=sns.color_palette('pastel'))
        plt.title('4. Payment Methods Preference', fontsize=14, fontweight='bold')
        plt.savefig('images/04_payment_methods.png', dpi=300)
        print("✅ Generated: images/04_payment_methods.png")
    except:
        print("⚠️ Skipping Payment Analysis (File missing)")

if __name__ == "__main__":
    conn = load_data_to_sql()
    if conn:
        analyze_rfm_segmentation(conn) # The new Senior Level chart
        analyze_payment_behavior(conn)
        conn.close()
        if os.path.exists(DB_PATH): os.remove(DB_PATH)
