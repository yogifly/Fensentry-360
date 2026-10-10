# FinSentry 360 - Plain-Language Guide

## What is FinSentry 360?

FinSentry 360 is a prototype for helping people and organizations identify
financial fraud before money is released and respond quickly when something
goes wrong.

It brings several protection ideas into one place:

- checking whether a payment looks suspicious;
- checking whether a recipient account looks risky;
- checking whether an invoice appears to have changed bank details;
- showing suspicious connections between accounts;
- recording an incident and starting a fast recovery process.

This is currently a demonstration product, not a live banking product.

## What the current prototype can demonstrate

### Payment Guard

A user enters payment details and a beneficiary ID. The system reviews signals
such as:

- unusually large amounts;
- a newly added recipient;
- a high transaction frequency;
- active phone calls or screen sharing;
- unusual typing or touch behavior;
- known complaints or mule-account indicators.

The system then shows a risk score and a recommendation such as approve,
review, or block.

### Corporate Guard

A company can upload a demo invoice. The system checks whether the payment
account and bank routing information match the registered vendor information.
If they do not match, the invoice receives a higher risk score and can be
marked as blocked in the prototype.

This is intended to demonstrate protection against invoice redirection and
vendor-payment fraud.

### Golden-Hour Rescue

If a user reports a suspicious transaction, the prototype:

1. records the incident;
2. marks the transaction as fraud reported;
3. simulates a request to freeze the recipient account;
4. creates an evidence report;
5. shows that recovery has started.

The freeze and recovery actions are demonstrations only. No bank account is
actually frozen.

### Dashboard

The dashboard is intended to give a security or finance team a quick overview
of:

- total transactions;
- high-risk transactions;
- blocked payments;
- fraud incidents;
- invoice activity;
- activity over time;
- risk distribution.

### Network view

The network view shows a simulated relationship between a user, a beneficiary,
and potentially suspicious accounts. It helps explain how money could move
through connected accounts.

## What the prototype is aiming to become

The long-term aim is to create a trusted fraud-defense platform for
individuals, finance teams, and security operations teams.

The intended product direction is:

1. **Prevent fraud early** by warning before a payment is approved.
2. **Protect organizations** from invoice and vendor-payment manipulation.
3. **Make investigations faster** by bringing transactions, beneficiaries,
   incidents, and evidence together.
4. **Improve response time** during the period immediately after suspected
   fraud.
5. **Give decision-makers understandable explanations**, not just a number.
6. **Create a repeatable audit trail** for reviews and investigations.

## Planned work

### Phase 1 - Improve the demonstration

- Make the screens more consistent and easier to understand.
- Add stronger sample data and more realistic demo scenarios.
- Add clearer explanations for every risk score.
- Improve invoice examples and document handling.
- Add better error messages and loading states.
- Add automated tests for the main user journeys.

### Phase 2 - Make it reliable for an internal pilot

- Add secure sign-in.
- Add different roles for finance users, investigators, and administrators.
- Keep each organization's information separate.
- Add a permanent audit history showing who did what and when.
- Add monitoring so failures are visible to the support team.
- Store reports and uploaded documents safely.
- Add backup and recovery procedures.

### Phase 3 - Connect approved external services

Only after security and legal approval, the product could connect to:

- payment providers;
- bank notification or freeze services;
- identity and account verification services;
- enterprise invoice systems;
- case-management and alerting systems.

Every external action should require clear authorization, logging, safe retry
behavior, and a way to stop or reverse the action where appropriate.

### Phase 4 - Build a governed fraud intelligence product

- Measure how often warnings are correct.
- Reduce unnecessary blocking of genuine payments.
- Monitor changes in fraud patterns.
- Review risk rules regularly.
- Document how decisions are made.
- Conduct privacy, security, legal, and regulatory reviews.

## How a non-technical person can demonstrate it

1. Open the deployed FinSentry 360 website.
2. Open **Payment Guard**.
3. Enter a demo amount and beneficiary ID.
4. Submit the payment for analysis.
5. Review the score, risk level, and reasons.
6. Open **Corporate Guard**.
7. Upload a demo invoice.
8. Review the vendor-account comparison.
9. Use **Block payment** to demonstrate the response action.
10. Open **Transactions**, **Fraud Incidents**, and **Dashboard** to see the
    stored activity.
11. Use **Golden-Hour Rescue** with the transaction ID created by Payment Guard
    to demonstrate the incident workflow.

## What the results mean

The results are risk indicators for demonstration purposes:

- **Low** means the prototype did not detect many warning signals.
- **Medium** means the payment or invoice deserves additional review.
- **High** means several warning signals were detected.
- **Critical** means the prototype recommends stopping or escalating the action.

These labels are not guarantees. A low score does not prove that something is
safe, and a high score does not prove that fraud occurred.

## What is not yet included

The current prototype does not provide:

- real money movement;
- real bank freezes;
- guaranteed fraud detection;
- a live connection to a bank;
- a replacement for a finance approval process;
- legal evidence or a legal filing;
- complete user security;
- full regulatory compliance;
- guaranteed permanent document storage;
- a production-grade fraud model.

The prototype should only use synthetic or approved test data. Real customer
financial information should not be uploaded until the product has completed
security, privacy, compliance, and legal reviews.

## How success will be measured

The future product should be evaluated using measurable outcomes:

- fewer fraudulent payments reaching approval;
- fewer genuine payments blocked by mistake;
- faster reporting after a suspected incident;
- faster investigator response;
- fewer invoice account-change fraud events;
- complete and searchable audit history;
- high service availability;
- secure handling of documents and personal information;
- positive feedback from finance and security teams.

## Decisions still needed

Before moving beyond the prototype, the product team should agree on:

- who the first users are;
- which countries and regulations apply;
- which payment and accounting systems must be supported;
- who is allowed to block or release a payment;
- when a warning requires human approval;
- how long data and reports should be retained;
- which external providers are approved;
- what level of false positives is acceptable;
- how incidents are escalated and closed.

## Final message

FinSentry 360 is designed to demonstrate a safer and faster way to respond to
financial fraud. Its next step is not simply adding more screens. The next
step is proving that the decisions are accurate, explainable, secure,
auditable, and safe to use in real business processes.

