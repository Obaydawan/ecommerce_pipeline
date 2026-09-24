# Automated E-Commerce Order & Revenue Pipeline

A production-style data pipeline that turns raw, multi-file e-commerce order data into a live, automatically-refreshable revenue dashboard — built on a modern cloud data stack (Snowflake + dbt) rather than a one-off notebook or spreadsheet.

**Live dashboard:** https://e-commercepipeline.streamlit.app/

---

## What this solves

Most small e-commerce businesses have order, payment, and product data scattered across raw exports with no reliable, tested pipeline turning it into trustworthy numbers. This project demonstrates that pipeline end-to-end: ingestion → a tested, documented transformation layer → a live dashboard — the same pattern used to automate order/revenue reporting for a real store, marketplace, or DTC brand.

---

## Architecture

```
  RAW CSVs (Olist order/item/product/customer/payment data)
        |
        v
  dbt seed  -->  SNOWFLAKE (raw tables, ecommerce_raw.staging)
        |
        v
  dbt staging models  -->  stg_orders, stg_order_items
        |                  (cleaned types, standardized columns, deduped)
        v
  dbt mart model  -->  orders_summary
        |              (joined, COALESCE-guarded aggregations)
        v
  dbt tests  -->  not_null / unique / accepted_values
        |          (data quality enforced before it ever reaches the dashboard)
        v
  STREAMLIT DASHBOARD (app/streamlit_app.py)
        |              connects live to Snowflake via .streamlit/secrets.toml
        v
  - Total order value tracked
  - Full orders table
  - Monthly revenue trend (Pandas .resample('ME'))
```

---

## Stack

| Layer | Tool |
|---|---|
| Warehouse | Snowflake |
| Transformation | dbt-core + dbt-snowflake |
| Orchestration (loading) | `dbt seed` |
| Dashboard | Streamlit, deployed on Streamlit Community Cloud |
| Data | [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) |

---

## What makes this production-style, not a tutorial clone

- **Tested, not just transformed** — every model has dbt tests (`not_null`, `unique`, `accepted_values`) enforced before data reaches the dashboard layer.
- **Layered transformation** — raw → staging → mart, not one giant query. Staging models isolate cleaning logic (`stg_orders`, `stg_order_items`) from business logic (`orders_summary`), so either layer can change independently.
- **Reliable aggregations** — `orders_summary` uses `COALESCE` guards so missing values don't silently break revenue totals.
- **Secrets handled properly** — Snowflake credentials live in `.streamlit/secrets.toml`, excluded from version control via `.gitignore`, never hardcoded.

---

## Run it yourself

```bash
git clone https://github.com/Obaydawan/ecommerce_pipeline
cd ecommerce_pipeline

# install dependencies
pip install dbt-core dbt-snowflake --break-system-packages

# configure your own Snowflake connection in ~/.dbt/profiles.yml, then:
dbt seed
dbt build

# add your own Snowflake credentials to .streamlit/secrets.toml, then:
streamlit run app/streamlit_app.py
```

---

## Available as a service

I build this exact kind of pipeline — automated order/revenue reporting connected live to your store's data — for e-commerce businesses who are still stitching numbers together manually every month. If your order, payment, or inventory data lives across disconnected exports and spreadsheets, I can turn it into a tested, always-current dashboard like this one.

**Get in touch:** [fiverr.com/obaydawan](https://www.fiverr.com/obaydawan)

---

## Related work

- [EmberRisk](https://github.com/Obaydawan/emberrisk) — wildfire risk intelligence ML pipeline
- [TransactSafe](https://banking-lakehouse-pipeline.streamlit.app) — banking fraud detection lakehouse (dbt + Airflow + Streamlit)
