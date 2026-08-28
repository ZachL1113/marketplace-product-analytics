-- DuckDB starter analysis for the Olist public dataset.
-- Run from the repository root after placing CSV files in data/raw/.

CREATE OR REPLACE VIEW orders AS
SELECT * FROM read_csv_auto('data/raw/olist_orders_dataset.csv', header = true);

CREATE OR REPLACE VIEW items AS
SELECT * FROM read_csv_auto('data/raw/olist_order_items_dataset.csv', header = true);

CREATE OR REPLACE VIEW customers AS
SELECT * FROM read_csv_auto('data/raw/olist_customers_dataset.csv', header = true);

CREATE OR REPLACE VIEW reviews AS
SELECT * FROM read_csv_auto('data/raw/olist_order_reviews_dataset.csv', header = true);

-- One row per order prevents multi-item orders from inflating order metrics.
CREATE OR REPLACE VIEW order_level AS
WITH item_agg AS (
    SELECT
        order_id,
        SUM(price) AS item_value,
        SUM(freight_value) AS freight_value,
        COUNT(*) AS item_count,
        COUNT(DISTINCT seller_id) AS seller_count
    FROM items
    GROUP BY 1
),
review_agg AS (
    SELECT order_id, AVG(review_score) AS review_score
    FROM reviews
    GROUP BY 1
)
SELECT
    o.*,
    c.customer_unique_id,
    c.customer_state,
    COALESCE(i.item_value, 0) AS item_value,
    COALESCE(i.freight_value, 0) AS freight_value,
    i.item_count,
    i.seller_count,
    r.review_score,
    o.order_status IN ('canceled', 'unavailable') AS is_cancelled,
    CASE
        WHEN o.order_delivered_customer_date IS NULL OR o.order_estimated_delivery_date IS NULL THEN NULL
        ELSE CAST(o.order_delivered_customer_date AS TIMESTAMP)
             <= CAST(o.order_estimated_delivery_date AS TIMESTAMP)
    END AS is_on_time
FROM orders o
LEFT JOIN item_agg i USING (order_id)
LEFT JOIN customers c USING (customer_id)
LEFT JOIN review_agg r USING (order_id);

SELECT
    COUNT(DISTINCT order_id) AS orders,
    SUM(CASE WHEN NOT is_cancelled THEN item_value ELSE 0 END) AS gmv,
    AVG(CAST(is_cancelled AS INTEGER)) AS cancellation_rate,
    AVG(CAST(is_on_time AS INTEGER)) AS on_time_delivery_rate,
    AVG(review_score) AS average_review_score
FROM order_level;

