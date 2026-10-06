-- Top regions by revenue
SELECT
    region,
    ROUND(SUM(total_revenue), 2) AS revenue
FROM retail_dev.gold.daily_region_sales
GROUP BY region
ORDER BY revenue DESC;

-- Daily revenue
SELECT
    order_date,
    ROUND(SUM(total_revenue), 2) AS daily_revenue
FROM retail_dev.gold.daily_region_sales
GROUP BY order_date
ORDER BY order_date;

-- Average order value by region
SELECT
    region,
    ROUND(AVG(average_order_value), 2) AS avg_order_value
FROM retail_dev.gold.daily_region_sales
GROUP BY region
ORDER BY avg_order_value DESC;
