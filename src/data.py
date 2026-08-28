"""Data loading utilities with an explicit synthetic demo fallback."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_FILES = {
    "orders": "olist_orders_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
}


def load_olist_data(raw_dir: str | Path = "data/raw") -> tuple[dict[str, pd.DataFrame], bool]:
    """Load Olist CSVs, or return a labelled synthetic fixture.

    Returns `(tables, is_demo)` so the user interface can never silently present
    synthetic records as public dataset results.
    """

    raw_path = Path(raw_dir)
    paths = {name: raw_path / filename for name, filename in REQUIRED_FILES.items()}
    if all(path.exists() for path in paths.values()):
        return {name: pd.read_csv(path) for name, path in paths.items()}, False
    return make_demo_data(), True


def make_demo_data() -> dict[str, pd.DataFrame]:
    """Create a small synthetic fixture for interface and metric development."""

    orders = pd.DataFrame(
        [
            ("o01", "c01", "delivered", "2026-01-01", "2026-01-05", "2026-01-06"),
            ("o02", "c02", "delivered", "2026-01-02", "2026-01-09", "2026-01-07"),
            ("o03", "c03", "delivered", "2026-01-04", "2026-01-08", "2026-01-09"),
            ("o04", "c04", "canceled", "2026-01-05", None, "2026-01-12"),
            ("o05", "c05", "delivered", "2026-01-08", "2026-01-15", "2026-01-13"),
            ("o06", "c06", "delivered", "2026-02-01", "2026-02-06", "2026-02-07"),
            ("o07", "c07", "delivered", "2026-02-03", "2026-02-08", "2026-02-08"),
            ("o08", "c08", "delivered", "2026-02-05", "2026-02-14", "2026-02-11"),
            ("o09", "c09", "delivered", "2026-02-10", "2026-02-13", "2026-02-15"),
            ("o10", "c10", "delivered", "2026-02-12", "2026-02-20", "2026-02-18"),
        ],
        columns=[
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )

    items = pd.DataFrame(
        [
            ("o01", 1, "p01", "s01", 80.0, 8.0),
            ("o02", 1, "p02", "s02", 45.0, 6.0),
            ("o03", 1, "p03", "s01", 120.0, 10.0),
            ("o04", 1, "p04", "s03", 35.0, 5.0),
            ("o05", 1, "p05", "s02", 90.0, 9.0),
            ("o06", 1, "p06", "s01", 70.0, 7.0),
            ("o07", 1, "p07", "s03", 55.0, 6.0),
            ("o08", 1, "p08", "s02", 130.0, 12.0),
            ("o09", 1, "p09", "s01", 60.0, 7.0),
            ("o10", 1, "p10", "s03", 75.0, 8.0),
        ],
        columns=["order_id", "order_item_id", "product_id", "seller_id", "price", "freight_value"],
    )

    customers = pd.DataFrame(
        [
            ("c01", "u01", "alpha", "SP"),
            ("c02", "u02", "beta", "RJ"),
            ("c03", "u03", "alpha", "SP"),
            ("c04", "u04", "gamma", "MG"),
            ("c05", "u02", "beta", "RJ"),
            ("c06", "u05", "delta", "PR"),
            ("c07", "u06", "alpha", "SP"),
            ("c08", "u07", "beta", "RJ"),
            ("c09", "u01", "alpha", "SP"),
            ("c10", "u08", "gamma", "MG"),
        ],
        columns=["customer_id", "customer_unique_id", "customer_city", "customer_state"],
    )

    reviews = pd.DataFrame(
        [
            ("r01", "o01", 5),
            ("r02", "o02", 2),
            ("r03", "o03", 5),
            ("r04", "o05", 2),
            ("r05", "o06", 5),
            ("r06", "o07", 4),
            ("r07", "o08", 1),
            ("r08", "o09", 5),
            ("r09", "o10", 2),
        ],
        columns=["review_id", "order_id", "review_score"],
    )

    return {"orders": orders, "items": items, "customers": customers, "reviews": reviews}

