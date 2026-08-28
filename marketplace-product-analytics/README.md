# Marketplace Product Analytics: Seller Health & Retention

An in-progress product analytics case study on how a marketplace team can identify high-impact seller issues, prioritise operational interventions, and define measurable product experiments.

The analysis is designed for the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), which contains approximately 100,000 anonymised marketplace orders. The public dataset is not redistributed in this repository.

## Project status

**In progress - August 2026**

Completed foundation:

- documented product problem and metric tree;
- reusable order-level metric pipeline with explicit grain handling;
- seller performance and health-scoring logic;
- interactive Streamlit dashboard scaffold;
- SQL starter analysis for DuckDB;
- unit tests and GitHub Actions CI;
- transparent demo mode using synthetic development fixtures.

Planned weekend deliverables:

- run the complete workflow on the Olist public dataset;
- validate metric definitions and data-quality edge cases;
- publish seller, category, delivery, and retention findings;
- complete the operational action queue and experiment proposal;
- deploy the dashboard to Streamlit Community Cloud.

## Product question

> Which sellers and operational issues should a marketplace team prioritise to improve delivery reliability and customer experience without unnecessarily restricting healthy supply?

The project separates three layers:

1. **Measurement** - define marketplace health consistently.
2. **Diagnosis** - locate seller, category, and delivery drivers.
3. **Decision** - translate findings into a prioritised intervention queue and an experiment plan.

## Metric tree

```text
Marketplace health
|-- Commercial activity
|   |-- Orders
|   |-- GMV
|   `-- Average order value
|-- Customer continuity
|   `-- Repeat-purchase rate
`-- Experience quality
    |-- On-time delivery rate
    |-- Cancellation rate
    `-- Average review score
```

Definitions and known limitations are documented in [`product/metric_definitions.md`](product/metric_definitions.md).

## Repository structure

```text
.
|-- app.py                       # Streamlit dashboard
|-- src/
|   |-- data.py                  # Olist loader and demo fixture
|   |-- metrics.py               # KPI and seller-level analysis
|   `-- scoring.py               # Seller health and action queue
|-- queries/core_metrics.sql     # DuckDB starter queries
|-- product/
|   |-- metric_definitions.md
|   `-- intervention_proposal.md
|-- tests/                       # Unit tests for metric logic
`-- data/raw/                    # Local Olist CSVs; ignored by Git
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Publish this repository

Create a public GitHub repository named `marketplace-product-analytics` without adding another README, licence, or `.gitignore`.

If you are working from this existing Git repository, push it directly:

```bash
git remote add origin https://github.com/ZachL1113/marketplace-product-analytics.git
git push -u origin main
```

If you downloaded the project archive, extract it and initialise the repository first:

```bash
git init -b main
git add .
git commit -m "Initialize marketplace product analytics case study"
git remote add origin https://github.com/ZachL1113/marketplace-product-analytics.git
git push -u origin main
```

Alternatively, use GitHub's **Add file -> Upload files** control to upload the extracted contents, including the hidden `.github` workflow folder.

The intended public URL is:

`https://github.com/ZachL1113/marketplace-product-analytics`

Without the Olist CSV files, the app runs in clearly labelled **demo mode** using a small synthetic fixture. To use the public data, download the dataset from Kaggle and place these files in `data/raw/`:

- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_customers_dataset.csv`
- `olist_order_reviews_dataset.csv`

## Tests

```bash
python -m unittest discover -s tests -v
```

## Decision principles

- Do not confuse correlation with causal impact.
- Do not rank low-volume sellers on unstable rates without a confidence adjustment.
- Keep scoring weights visible and adjustable.
- Pair every intervention metric with commercial and seller-supply guardrails.
- Preserve traceability from dashboard conclusions to metric definitions and source data.

## Data acknowledgement

The Olist dataset contains anonymised historical Brazilian marketplace orders from 2016 to 2018. It is used as a product analytics case dataset, not as evidence about the current Brazilian or Southeast Asian e-commerce market.
