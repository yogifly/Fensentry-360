# FinSentry 360 - Website Demo Steps

This guide explains what to do after opening the FinSentry 360 website.

> This is a simulation. Do not enter real bank details, customer information,
> invoices, or payment data.

## 1. Open the dashboard

When the website opens, you will see the main dashboard.

Review:

- Total transactions
- High-risk transactions
- Blocked payments
- Fraud incidents
- Invoice activity
- Risk distribution
- Recent activity

If the dashboard contains demo data, the application is connected and ready.

## 2. Test Payment Guard

Open **Payment Guard** from the left navigation.

Fill in:

| Field | Value |
|---|---:|
| Amount | `50000` |
| Beneficiary ID | `2` |
| Active phone call | Turn on |
| Screen sharing | Turn on |
| Typing deviation | `0.82` |
| Touch jitter | `0.76` |
| Touch pressure | `0.70` |
| Session duration | `45` |

Then:

1. Click **Analyze payment**.
2. Wait for the risk result.
3. Review the risk score.
4. Review the risk level.
5. Read the reasons shown by the system.
6. Review the recommended action.
7. Note the transaction ID shown or returned by the result.

The result is simulated. No payment is made.

### Test an invalid beneficiary ID

Return to the beneficiary field and enter:

```text
9999
```

Move to another field or submit the form. The website should show that the
beneficiary ID was not found.

## 3. Test Corporate Guard

Open **Corporate Guard** from the left navigation.

Upload a demo invoice containing values similar to these:

```text
Vendor: Demo Trading Company
Invoice Number: INV-DEMO-001
Amount: 245000
Account: 9876543210
IFSC: HDFC0005678
```

You can use a text-compatible demo file or a PDF containing the same
information.

Then:

1. Click **Analyze invoice**.
2. Review the invoice amount.
3. Review the invoice account and IFSC.
4. Read the mismatch warnings.
5. Review the invoice risk score and risk level.
6. Click **Block payment**.
7. Confirm that the button changes to **Payment blocked**.

The prototype compares the uploaded invoice with these registered demo values:

```text
Registered account: 1234567890
Registered IFSC: HDFC0001234
```

The values in the sample invoice are different, so the invoice should be
reported as risky. No real payment is blocked.

## 4. Test Golden-Hour Rescue

Use the transaction ID created during the Payment Guard test.

Then:

1. Open **Golden-Hour Rescue** or click **Report fraud** from Payment Guard.
2. Enter the transaction ID.
3. Enter this description:

   ```text
   Demo social engineering incident for testing.
   ```

4. Click the rescue/report button.
5. Review the incident ID.
6. Review the transaction locked message.
7. Review the simulated freeze request.
8. Review the evidence report status.
9. Note the report hash if displayed.
10. Review the recovery status.

The bank freeze and recovery actions are simulated only.

## 5. Review the saved transaction

Open **Transactions**.

Find the transaction you just analyzed. Review:

- Transaction reference
- Amount
- Beneficiary ID
- Risk score
- Risk level
- Status
- Time created

## 6. Review the fraud incident

Open **Fraud Incidents**.

Find the incident created by the rescue test. Review:

- Incident reference
- Transaction ID
- Fraud type
- Fraud score
- Incident status
- Recovery status
- Time created

## 7. Test Network Analysis

Open **Network Analysis**.

Enter beneficiary ID:

```text
2
```

Then click the search or analyze button.

Review the displayed relationship graph, including:

- User
- Beneficiary
- Connected or secondary account
- Relationship lines
- Risk indicators

You can also test beneficiary ID `3`, which represents another high-risk demo
beneficiary.

## 8. Return to the dashboard

Open **Dashboard** again and confirm that the activity has changed.

You should be able to see updated:

- Transaction totals
- Risk distribution
- Activity chart
- Recent incidents
- Blocked or reported activity

## Suggested demo order

For the clearest demonstration, use this order:

1. Dashboard
2. Payment Guard
3. Corporate Guard
4. Golden-Hour Rescue
5. Transactions
6. Fraud Incidents
7. Network Analysis
8. Dashboard again

## If something does not load

Refresh the page once and try again. If the issue continues, contact the
person who deployed the application. Do not enter real financial information
while troubleshooting.

