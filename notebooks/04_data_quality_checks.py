# Databricks notebook source
# MAGIC %md
# MAGIC # 04 - Data quality checks

# COMMAND ----------

from pyspark.sql import functions as F

CATALOG = "retail_dev"
df = spark.table(f"{CATALOG}.silver.orders")

checks = {
    "row_count": df.count(),
    "null_order_id": df.filter(F.col("order_id").isNull()).count(),
    "duplicate_order_id": (
        df.groupBy("order_id").count().filter(F.col("count") > 1).count()
    ),
    "negative_revenue": df.filter(F.col("net_amount") < 0).count()
}

print(checks)

assert checks["row_count"] > 0, "No Silver records found"
assert checks["null_order_id"] == 0, "Null order IDs found"
assert checks["duplicate_order_id"] == 0, "Duplicate order IDs found"
assert checks["negative_revenue"] == 0, "Negative revenue found"

print("All data quality checks passed.")
