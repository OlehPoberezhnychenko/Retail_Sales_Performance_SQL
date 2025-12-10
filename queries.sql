-- 1. CALCULATE DELIVERY DELAYS BY STATE
SELECT 
    c.customer_state,
    AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)) as avg_delivery_time
FROM olist_orders_dataset o
JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY 1
ORDER BY 2 DESC;

-- 2. REVENUE PARETO ANALYSIS (Top Categories)
WITH Category_Sales AS (
    SELECT 
        p.product_category_name,
        SUM(oi.price) as total_revenue
    FROM olist_order_items_dataset oi
    JOIN olist_products_dataset p ON oi.product_id = p.product_id
    GROUP BY 1
)
SELECT *,
    RANK() OVER (ORDER BY total_revenue DESC) as rank
FROM Category_Sales
LIMIT 10;
