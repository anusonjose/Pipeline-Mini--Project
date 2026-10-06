# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Silver transformation
# MAGIC Clean, validate, deduplicate and enrich orders.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

CATALOG = "retail_dev"

orders = spark.table(f"{CATALOG}.bronze.orders_raw")
customers = spark.read.option("header", True).option("inferSchema", True).csv(
    "dbfs:/FileStore/retail/customers.csv"
)

# COMMAND ----------

orders_clean = (
    orders
    .withColumn("order_date", F.to_date("order_date"))
    .withColumn("updated_at", F.to_timestamp("updated_at"))
    .withColumn("quantity", F.col("quantity").cast("int"))
    .withColumn("unit_price", F.col("unit_price").cast("double"))
    .filter(F.col("order_id").isNotNull())
    .filter(F.col("customer_id").isNotNull())
    .filter(F.col("quantity") > 0)
    .filter(F.col("unit_price") >= 0)
)

# Keep the latest version of each order.
w = Window.partitionBy("order_id").orderBy(F.col("updated_at").desc_nulls_last())

orders_dedup = (
    orders_clean
    .withColumn("_rn", F.row_number().over(w))
    .filter(F.col("_rn") == 1)
    .drop("_rn")
)

# COMMAND ----------

silver = (
    orders_dedup.alias("o")
    .join(customers.alias("c"), "customer_id", "left")
    .withColumn("net_amount", F.col("quantity") * F.col("unit_price"))
    .select(
        "order_id",
        "customer_id",
        "customer_name",
        "region",
        "segment",
        "order_date",
        "updated_at",
        "product_category",
        "quantity",
        "unit_price",
        "net_amount"
    )
)

silver.write.format("delta").mode("overwrite").option(
    "overwriteSchema", "true"
).saveAsTable(f"{CATALOG}.silver.orders")

print(f"Silver records: {silver.count()}")
