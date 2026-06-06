# Incident Report: Borealis

**Date:** 2026-03-14

## Summary
Borealis was a customer-facing outage that delayed audit exports and slowed ingestion.

## Root cause
The immediate cause was queue saturation in the ingestion service caused by the **nightly-reconcile** batch job.

## Mitigation
- Paused the **nightly-reconcile** batch job.
- Increased the worker pool from **12** to **20**.
- Enabled a circuit breaker on the ingestion path.

## Follow-up
- Missing backpressure was identified as the underlying engineering gap.
- A post-incident task was opened as **ENG-442**.

## Customer impact
Audit exports were delayed by **18 minutes**.
