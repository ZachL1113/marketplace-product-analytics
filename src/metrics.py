"""Metric definitions for order, customer, and seller analysis."""

from __future__ import annotations

import math

import pandas as pd


CANCELLED_STATUSES = {"canceled", "unavailable"}


def prepare_order_level(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Build one row per order before calculating marketplace KPIs.

    Aggregating items first prevents multi-item orders from inflating order
    counts, cancellation rates, or customer counts.
    """

    orders = tables["orders"].copy()
    items = tables["items"].copy()
    customers = tables["customers"].copy()
    reviews = tables["reviews"].copy()

    item_agg = (
        items.groupby("order_id", as_index=False)
        .agg(
            item_value=("price", "sum"),
            freight_value=("freight_value", "sum"),
            item_count=("order_item_id", "count"),
            seller_count=("seller_id", "nunique"),
        )
    )
    review_agg = reviews.groupby("order_id", as_index=False).agg(review_score=("review_score", "mean"))

    frame = orders.merge(item_agg, on="order_id", how="left")
    frame = frame.merge(customers, on="customer_id", how="left")
    frame = frame.merge(review_agg, on="order_id", how="left")

    for column in (
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ):
        frame[column] = pd.to_datetime(frame[column], errors="coerce")

    frame["item_value"] = frame["item_value"].fillna(0.0)
    frame["freight_value"] = frame["freight_value"].fillna(0.0)
    frame["is_cancelled"] = frame["order_status"].isin(CANCELLED_STATUSES)
    has_delivery_measure = frame["order_delivered_customer_date"].notna() & frame[
        "order_estimated_delivery_date"
    ].notna()
    frame["is_on_time"] = pd.NA
    frame.loc[has_delivery_measure, "is_on_time"] = (
        frame.loc[has_delivery_measure, "order_delivered_customer_date"]
        <= frame.loc[has_delivery_measure, "order_estimated_delivery_date"]
    )
    frame["delivery_delay_days"] = (
        frame["order_delivered_customer_date"] - frame["order_estimated_delivery_date"]
    ).dt.days
    return frame


def calculate_kpis(order_level: pd.DataFrame) -> dict[str, float]:
    """Calculate top-level metrics from an order-grain table."""

    active = order_level.loc[~order_level["is_cancelled"]]
    completed_with_measure = order_level.loc[order_level["is_on_time"].notna()]

    unique_customer_orders = (
        active.dropna(subset=["customer_unique_id"])
        .groupby("customer_unique_id")["order_id"]
        .nunique()
    )
    repeat_rate = float((unique_customer_orders > 1).mean()) if len(unique_customer_orders) else math.nan
    on_time_rate = (
        float(completed_with_measure["is_on_time"].astype(float).mean())
        if len(completed_with_measure)
        else math.nan
    )
    gmv = float(active["item_value"].sum())
    active_orders = int(active["order_id"].nunique())

    return {
        "orders": float(order_level["order_id"].nunique()),
        "gmv": gmv,
        "aov": gmv / active_orders if active_orders else math.nan,
        "repeat_purchase_rate": repeat_rate,
        "on_time_delivery_rate": on_time_rate,
        "cancellation_rate": float(order_level["is_cancelled"].mean()),
        "average_review_score": float(order_level["review_score"].mean()),
    }


def build_seller_performance(tables: dict[str, pd.DataFrame], order_level: pd.DataFrame) -> pd.DataFrame:
    """Create seller-level performance metrics with order exposure preserved."""

    order_fields = order_level[
        ["order_id", "is_cancelled", "is_on_time", "review_score", "delivery_delay_days"]
    ]
    seller_orders = (
        tables["items"]
        .groupby(["seller_id", "order_id"], as_index=False)
        .agg(item_value=("price", "sum"), item_count=("order_item_id", "count"))
        .merge(order_fields, on="order_id", how="left")
    )

    result = (
        seller_orders.groupby("seller_id", as_index=False)
        .agg(
            order_count=("order_id", "nunique"),
            gmv=("item_value", "sum"),
            average_review_score=("review_score", "mean"),
            on_time_delivery_rate=("is_on_time", lambda s: pd.to_numeric(s, errors="coerce").mean()),
            cancellation_rate=("is_cancelled", "mean"),
            average_delay_days=("delivery_delay_days", "mean"),
        )
    )
    return result

