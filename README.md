### 3. Customer Segmentation (RFM Analysis)
*Using "Recency, Frequency, Monetary" analysis to classify users.*
![RFM Segments](images/03_rfm_segments.png)

### 💻 Advanced SQL Logic (RFM)
*I used SQL Window Functions (`NTILE`) to score customers automatically:*
```sql
SELECT 
    customer_unique_id,
    NTILE(5) OVER (ORDER BY last_order) as r_score,
    NTILE(5) OVER (ORDER BY frequency) as f_score,
    NTILE(5) OVER (ORDER BY monetary) as m_score
FROM customer_stats;
