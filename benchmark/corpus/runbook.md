# Nimbus Support Runbook

## Incident escalation flow
1. Confirm customer impact.
2. Page the on-call engineer.
3. Open an incident document.
4. Post a customer-facing status update.
5. Close with a postmortem and follow-up tasks.

## Severity targets
- **P1**: response within **20 minutes**
- **P2**: response within **2 hours**
- **P3**: response within **1 business day**

## Audit export failure
If the audit export queue backs up:
- check the **audit-exporter** queue depth
- pause **nightly-reconcile** if needed
- offer the customer a **manual CSV download**

## Payment webhook failure
If the payment webhook fails:
- wait **15 minutes**
- retry once
- if it still fails, open **SEV2**
