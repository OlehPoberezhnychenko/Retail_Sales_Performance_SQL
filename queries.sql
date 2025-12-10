-- 1. CALCULATE DELIVERY DELAYS BY STATE
-- Identifying logistics bottlenecks by region
SELECT 
    c.customer_state,
    AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)) as avg_delivery_days
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 2 DESC;

-- 2. REVENUE PARETO ANALYSIS (Top Categories)
-- Finding the 20% of categories that drive 80% of revenue
WITH Category_Sales AS (
    SELECT 
        p.product_category_name,
        SUM(i.price) as total_revenue
    FROM order_items i
    JOIN products p ON i.product_id = p.product_id
    GROUP BY 1
)
SELECT *,
    RANK() OVER (ORDER BY total_revenue DESC) as rank
FROM Category_Sales
LIMIT 10;

-- 3. ADVANCED CUSTOMER SEGMENTATION (RFM)
-- Calculating Recency, Frequency, and Monetary scores per user
WITH customer_stats AS (
    SELECT 
        c.customer_unique_id,
        MAX(o.order_purchase_timestamp) as last_order,
        COUNT(o.order_id) as frequency,
        SUM(p.payment_value) as monetary
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id  -- FIXED: Added this join to get Unique ID
    JOIN payments p ON o.order_id = p.order_id
    GROUP BY 1
),
rfm_scores AS (
    SELECT 
        customer_unique_id,
        NTILE(5) OVER (ORDER BY last_order) as r_score,
        NTILE(5) OVER (ORDER BY frequency) as f_score,
        NTILE(5) OVER (ORDER BY monetary) as m_score
    FROM customer_stats
)
SELECT 
    r_score || f_score || m_score as rfm_profile,
    COUNT(*) as customer_count
FROM rfm_scores
GROUP BY 1
ORDER BY 2 DESC;
