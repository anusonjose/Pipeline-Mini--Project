# Interview guide

## Explain the project

"I built a retail data pipeline using Azure Databricks and ADLS Gen2. Order data comes from a REST API and customer reference data comes from CSV. The raw API data is stored in the Bronze layer. Databricks PySpark cleans, validates and deduplicates the data in Silver, then joins customer attributes. The Gold layer produces daily regional revenue metrics. The pipeline is designed for incremental processing using an updated timestamp watermark and Delta MERGE."

## Why Bronze/Silver/Gold?

Bronze preserves source data, Silver contains cleaned/conformed data, and Gold contains business-ready aggregates.

## How do you avoid duplicates?

Use the business key `order_id`, select the latest record by `updated_at`, and use Delta MERGE for production incremental upserts.

## How do you avoid missing records?

Persist a successful watermark only after processing succeeds. For APIs, use pagination/cursors and, where supported, a small overlap window.

## How do you secure credentials?

Use Databricks secrets or Azure Key Vault-backed secrets. Prefer managed identity/service principals rather than hard-coded credentials.

## What would you add in production?

Pagination, retry/backoff, API rate-limit handling, quarantine records, schema monitoring, Unity Catalog permissions, ADF orchestration, job alerts, CI/CD, and Power BI.
