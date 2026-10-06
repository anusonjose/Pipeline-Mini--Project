# Setup

## 1. ADLS

Create an ADLS Gen2 storage account and containers/folders:

```text
bronze/
silver/
gold/
```

Grant the Databricks identity appropriate Storage Blob Data permissions.

## 2. Upload demo files

For a quick demo, upload:

```text
data/customers.csv
data/orders_api_sample.json
```

to a Databricks-accessible location such as:

```text
dbfs:/FileStore/retail/
```

## 3. Create catalog and schemas

```sql
CREATE CATALOG IF NOT EXISTS retail_dev;
CREATE SCHEMA IF NOT EXISTS retail_dev.bronze;
CREATE SCHEMA IF NOT EXISTS retail_dev.silver;
CREATE SCHEMA IF NOT EXISTS retail_dev.gold;
```

## 4. Run notebooks

Run in this order:

```text
01_bronze_ingestion
02_silver_transform
03_gold_aggregation
04_data_quality_checks
```

## 5. Production API

Create a Databricks secret:

```text
scope: retail-project
key: api-token
```

Then provide the API URL as a job parameter.

Never commit the token.
