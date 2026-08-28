# Product proposal: at-risk seller intervention workflow

## Problem

Marketplace experience issues can be concentrated among a limited number of sellers, while operations teams have finite review capacity. Raw defect rates alone can over-prioritise tiny sellers or overlook high-exposure sellers with moderate but costly deterioration.

## User and job to be done

**Primary user:** seller operations analyst or category operations manager.

**Job:** identify sellers whose combination of customer-experience risk and commercial exposure merits human review, understand the leading issue, and select a proportionate intervention.

## Proposed workflow

1. Monitor delivery, cancellation, rating, and exposure metrics.
2. Flag sellers below an adjustable health threshold.
3. Rank the review queue by experience risk and GMV exposure.
4. Display the leading issue and supporting order records.
5. Record the selected intervention and follow-up date.
6. Measure operational and marketplace guardrails after rollout.

## Intervention ladder

- Diagnostic message and self-serve guidance.
- Dispatch-SLA or inventory review.
- Temporary monitoring period with operational support.
- Targeted traffic or listing controls only after human review.

## Experiment outline

**Hypothesis:** a targeted diagnostic intervention for eligible high-risk sellers improves delivery reliability without materially reducing healthy marketplace activity.

**Unit:** seller-level randomisation among eligible sellers, where sample size permits.

**Primary metric:** on-time delivery rate over a predefined follow-up window.

**Secondary metrics:** average review score, cancellation rate, repeated operational defects.

**Guardrails:** GMV, active seller rate, seller support contacts, customer refund rate.

**Risks:** selection bias, spillovers across logistics providers, seasonal category mix, and insufficient power among low-volume sellers.

