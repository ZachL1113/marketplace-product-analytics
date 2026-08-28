"""Transparent seller health scoring and action-priority rules."""

from __future__ import annotations

import numpy as np
import pandas as pd


DEFAULT_WEIGHTS = {
    "delivery": 0.40,
    "reviews": 0.30,
    "cancellations": 0.20,
    "volume_confidence": 0.10,
}


def add_seller_health_score(
    seller_frame: pd.DataFrame, weights: dict[str, float] | None = None
) -> pd.DataFrame:
    """Add a 0-100 health score whose components remain inspectable.

    The score supports prioritisation; it is not presented as a causal model or
    a production policy. Missing experience metrics receive neutral values.
    """

    chosen = DEFAULT_WEIGHTS.copy()
    if weights:
        chosen.update(weights)
    total = sum(chosen.values())
    if not np.isclose(total, 1.0):
        raise ValueError(f"Weights must sum to 1.0, got {total:.3f}")

    frame = seller_frame.copy()
    delivery = frame["on_time_delivery_rate"].fillna(0.5).clip(0, 1)
    reviews = ((frame["average_review_score"].fillna(3.0) - 1.0) / 4.0).clip(0, 1)
    cancellations = (1.0 - frame["cancellation_rate"].fillna(0.0)).clip(0, 1)
    max_orders = max(float(frame["order_count"].max()), 1.0)
    confidence = np.log1p(frame["order_count"].astype(float)) / np.log1p(max_orders)

    frame["health_score"] = 100.0 * (
        chosen["delivery"] * delivery
        + chosen["reviews"] * reviews
        + chosen["cancellations"] * cancellations
        + chosen["volume_confidence"] * confidence
    )
    frame["health_score"] = frame["health_score"].round(1)
    return frame


def build_action_queue(scored: pd.DataFrame, threshold: float = 65.0) -> pd.DataFrame:
    """Prioritise unhealthy sellers by commercial exposure and suggest a review path."""

    queue = scored.loc[scored["health_score"] < threshold].copy()

    def action(row: pd.Series) -> str:
        if row["cancellation_rate"] >= 0.10:
            return "Review inventory and fulfilment controls"
        if pd.notna(row["on_time_delivery_rate"]) and row["on_time_delivery_rate"] < 0.80:
            return "Review dispatch SLA and logistics support"
        if pd.notna(row["average_review_score"]) and row["average_review_score"] < 3.5:
            return "Audit product quality and listing accuracy"
        return "Manual operations review"

    queue["suggested_action"] = queue.apply(action, axis=1)
    queue["priority_score"] = ((100.0 - queue["health_score"]) * np.log1p(queue["gmv"])).round(1)
    return queue.sort_values(["priority_score", "gmv"], ascending=False).reset_index(drop=True)

