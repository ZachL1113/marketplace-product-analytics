# Metric definitions

## Unit of analysis

Top-level metrics are calculated from one row per order. Item records are aggregated before joining to orders so multi-item and multi-seller orders do not inflate counts.

## Core metrics

| Metric | Definition | Decision use | Limitation |
| --- | --- | --- | --- |
| Orders | Distinct order IDs across all statuses | Activity baseline | Includes cancelled orders unless filtered |
| GMV | Item price from non-cancelled orders; freight excluded | Commercial exposure | Not net revenue or realised margin |
| AOV | GMV divided by non-cancelled orders | Basket-level activity | Sensitive to category mix |
| Repeat-purchase rate | Share of identifiable customers with more than one non-cancelled order | Customer continuity | Historical identity resolution may be imperfect |
| On-time delivery | Actual delivery on or before estimated delivery date | Promise reliability | Available only for measurable delivered orders |
| Cancellation rate | Share of orders with cancelled or unavailable status | Fulfilment friction | Does not establish seller responsibility |
| Average review | Mean order review score | Customer experience | Reviews may be missing non-randomly |

## Seller attribution

An order fulfilled by multiple sellers contributes one exposed order to each participating seller. The shared delivery outcome is therefore an operational signal, not proof that every seller caused the delay.

## Interpretation guardrails

- Associations between delivery and ratings or repeat purchasing are not causal effects.
- Low-volume seller rates require confidence adjustment or minimum-volume filters.
- Health-score weights express operational priorities and should be sensitivity-tested.
- A production policy would require additional seller, logistics, margin, and support-cost data.

