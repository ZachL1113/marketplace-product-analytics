"""Streamlit dashboard for the marketplace product analytics case."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data import load_olist_data
from src.metrics import build_seller_performance, calculate_kpis, prepare_order_level
from src.scoring import add_seller_health_score, build_action_queue


st.set_page_config(page_title="Marketplace Seller Health", page_icon="📊", layout="wide")


@st.cache_data
def load_analysis() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float], bool]:
    tables, is_demo = load_olist_data()
    order_level = prepare_order_level(tables)
    seller = build_seller_performance(tables, order_level)
    return order_level, seller, calculate_kpis(order_level), is_demo


order_level, seller_base, kpis, is_demo = load_analysis()

st.title("Marketplace Seller Health & Retention")
st.caption("From metric definition to operational prioritisation")
if is_demo:
    st.warning(
        "Demo mode: this interface is using a small synthetic development fixture. "
        "Place the four Olist CSV files in data/raw to run the public dataset analysis."
    )

with st.sidebar:
    st.header("Seller health weights")
    delivery_weight = st.slider("Delivery reliability", 0, 100, 40, 5)
    review_weight = st.slider("Customer reviews", 0, 100, 30, 5)
    cancellation_weight = st.slider("Cancellation control", 0, 100, 20, 5)
    volume_weight = st.slider("Volume confidence", 0, 100, 10, 5)
    total = delivery_weight + review_weight + cancellation_weight + volume_weight
    st.caption(f"Total weight: {total}%")

weights = {
    "delivery": delivery_weight / 100,
    "reviews": review_weight / 100,
    "cancellations": cancellation_weight / 100,
    "volume_confidence": volume_weight / 100,
}

if total != 100:
    st.error("Weights must sum to 100% before the seller score can be calculated.")
    st.stop()

seller = add_seller_health_score(seller_base, weights)
queue = build_action_queue(seller)

overview, diagnostics, actions, definitions = st.tabs(
    ["Executive overview", "Seller diagnostics", "Action queue", "Definitions"]
)

with overview:
    row1 = st.columns(4)
    row1[0].metric("Orders", f"{kpis['orders']:,.0f}")
    row1[1].metric("GMV", f"R$ {kpis['gmv']:,.0f}")
    row1[2].metric("Average order value", f"R$ {kpis['aov']:,.1f}")
    row1[3].metric("Repeat-purchase rate", f"{kpis['repeat_purchase_rate']:.1%}")

    row2 = st.columns(3)
    row2[0].metric("On-time delivery", f"{kpis['on_time_delivery_rate']:.1%}")
    row2[1].metric("Cancellation rate", f"{kpis['cancellation_rate']:.1%}")
    row2[2].metric("Average review", f"{kpis['average_review_score']:.2f} / 5")

    monthly = (
        order_level.assign(month=order_level["order_purchase_timestamp"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .agg(orders=("order_id", "nunique"), gmv=("item_value", "sum"))
    )
    st.plotly_chart(
        px.line(monthly, x="month", y="orders", markers=True, title="Monthly order activity"),
        use_container_width=True,
    )

with diagnostics:
    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            px.scatter(
                seller,
                x="on_time_delivery_rate",
                y="average_review_score",
                size="gmv",
                color="health_score",
                hover_name="seller_id",
                color_continuous_scale="RdYlGn",
                title="Seller experience and commercial exposure",
            ),
            use_container_width=True,
        )
    with right:
        st.plotly_chart(
            px.bar(
                seller.nlargest(15, "gmv").sort_values("gmv"),
                x="gmv",
                y="seller_id",
                orientation="h",
                color="health_score",
                color_continuous_scale="RdYlGn",
                title="Highest-exposure sellers",
            ),
            use_container_width=True,
        )

    st.dataframe(
        seller.sort_values("gmv", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

with actions:
    st.subheader("Operational review queue")
    st.write(
        "The queue ranks sellers below the selected health threshold by the combination "
        "of experience risk and GMV exposure. It supports human review; it is not an automated enforcement policy."
    )
    if queue.empty:
        st.success("No sellers fall below the current health threshold.")
    else:
        st.dataframe(queue, use_container_width=True, hide_index=True)
        st.download_button(
            "Download review queue",
            queue.to_csv(index=False).encode("utf-8"),
            "seller_action_queue.csv",
            "text/csv",
        )

with definitions:
    st.markdown(
        """
        - **GMV:** item value from non-cancelled orders; freight excluded.
        - **On-time delivery:** actual delivery date on or before the promised date, among measurable delivered orders.
        - **Repeat-purchase rate:** share of identifiable customers with more than one non-cancelled order.
        - **Seller health score:** transparent weighted index for prioritisation, not a causal model.
        - **Demo mode:** synthetic records are used only to verify interface and metric behaviour.
        """
    )

