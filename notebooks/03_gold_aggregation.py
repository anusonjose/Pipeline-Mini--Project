# Databricks notebook source
# MAGIC %md
# MAGIC # 03 - Gold aggregation
# MAGIC Create daily regional revenue metrics.

# COMMAND ----------

from pyspark.sql import functions as F

CATALOG = "retail_dev"

orders = spark.table(f"{CATALOG}.silver.orders")

gold = (
    orders
    .groupBy("order_date", "region")
    .agg(
        F.countDistinct("order_id").alias("order_count"),
        F.countDistinct("customer_id").alias("customer_count"),
        F.round(F.sum("net_amount"), 2).alias("total_revenue"),
        F.round(F.avg("net_amount"), 2).alias("average_order_value")
    )
)

gold.write.format("delta").mode("overwrite").option(
    "overwriteSchema", "true"
).saveAsTable(f"{CATALOG}.gold.daily_region_sales")

display(gold.orderBy("order_date", "region"))
