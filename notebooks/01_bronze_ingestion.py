# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Bronze ingestion
# MAGIC Fetch orders from a REST API and store raw records as Delta.

# COMMAND ----------

import requests
from datetime import datetime, timezone

# Replace with a real secret-backed value in Databricks.
API_URL = dbutils.widgets.get("api_url") if "api_url" in [w.name for w in dbutils.widgets.getAll()] else ""

CATALOG = "retail_dev"
BRONZE_SCHEMA = "bronze"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{BRONZE_SCHEMA}")

# COMMAND ----------

# For the demo, if API_URL is empty, use the bundled sample file.
if API_URL:
    token = dbutils.secrets.get(scope="retail-project", key="api-token")
    response = requests.get(
        API_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=60
    )
    response.raise_for_status()
    records = response.json()
else:
    records = [
        r.asDict()
        for r in spark.read.json("dbfs:/FileStore/retail/orders_api_sample.json").collect()
    ]

# COMMAND ----------

ingestion_ts = datetime.now(timezone.utc).isoformat()

df = spark.createDataFrame(records).withColumn(
    "ingestion_timestamp",
    __import__("pyspark").sql.functions.current_timestamp()
)

(
    df.write
      .format("delta")
      .mode("append")
      .saveAsTable(f"{CATALOG}.{BRONZE_SCHEMA}.orders_raw")
)

print(f"Bronze ingestion completed: {df.count()} records")
