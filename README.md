# FinSentry 360

FinSentry 360 is a fraud-defense MVP that demonstrates how suspicious payments,
beneficiary risk, invoice anomalies, and post-incident rescue actions can be
managed from one dashboard.

> **Safety notice:** This repository is a prototype. Payment execution, bank
> freezes, beneficiary relationships, recovery actions, and evidence workflows
> are simulated. It must not be connected to real banking, payment, or
> law-enforcement systems without a separate security, compliance, and
> production-readiness program.

## Contents

- [New user demo guide](DEMO_GUIDE.md)
- [Product scope](#product-scope)
- [Architecture](#architecture)
- [Repository structure](#repository-structure)
- [Backend](#backend)
- [Frontend](#frontend)
- [Data model](#data-model)
- [Main user workflows](#main-user-workflows)
- [Configuration](#configuration)
- [Run locally](#run-locally)
- [Testing](#testing)
- [Render deployment](#render-deployment)
- [API reference](#api-reference)
- [Security and operational limitations](#security-and-operational-limitations)
- [Roadmap](#roadmap)

## Product scope

The MVP contains:

1. **Payment Guard** - scores a proposed transaction using amount, beneficiary,
   behavioral, device/session, and velocity signals.
2. **Beneficiary validation** - validates an ID and displays demo beneficiary
   details, risk level, and known-mule status.
3. **Corporate Guard** - accepts a PDF or text-compatible invoice fixture,
   extracts invoice values, compares account and IFSC values with registered
   vendor values, and calculates invoice risk.
4. **Golden-Hour Rescue** - creates a fraud incident, simulates a bank freeze,
   generates a hashed evidence report, and marks recovery as initiated.
5. **Dashboard activity** - displays stored transactions, risk distribution,
   incidents, invoice totals, and recent activity.
6. **Network Analysis** - displays a simulated beneficiary/mule relationship
   graph.
7. **Transactions and incidents** - lists records persisted by the backend.

## Architecture

```text
React + TypeScript + Vite + Tailwind
              |
              | Axios / JSON / multipart uploads
              v
FastAPI + SQLAlchemy
              |
              +--> SQLite for local development
              |
              +--> PostgreSQL/Supabase for hosted deployment
              |
              +--> simulated risk, invoice, rescue, graph, and evidence services
```

The frontend is a static Vite application. The backend is an independent
FastAPI web service. The database is accessed only by the backend.

## Repository structure

```text
FinSentry-360/
├── Backend/
│   ├── app/
│   │   ├── api/routes.py              # HTTP endpoints
│   │   ├── config/settings.py         # environment configuration
│   │   ├── database/database.py       # SQLAlchemy engine/session
│   │   ├── database/models.py         # persistence models
│   │   ├── schemas/api.py             # request schemas
│   │   ├── services/                  # risk, invoice, graph, rescue services
│   │   └── seed/seed_database.py      # demo data
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── Frontend/
│   ├── src/App.tsx                    # routes and screens
│   ├── src/services/api.ts            # Axios API client and mock mode
│   ├── src/types.ts                   # TypeScript response types
│   ├── package.json
│   ├── .env.example
│   └── README.md
├── README.md
└── NON_TECHNICAL_README.md
```

Generated files, credentials, local databases, reports, dependencies, and
build output are excluded by [Backend/.gitignore](Backend/.gitignore) and
[Frontend/.gitignore](Frontend/.gitignore).

## Backend

### Technology

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite locally
- PostgreSQL through `psycopg2-binary`
- Pydantic request validation
- `python-dotenv` configuration loading
- ReportLab evidence PDF generation
- NetworkX relationship graph generation
- pandas, NumPy, scikit-learn, and XGBoost dependencies for prototype
  analytics/dataset work
- PyMuPDF, pdfplumber, pytesseract, and OpenCV dependencies for invoice
  processing experiments

### Backend behavior

The risk engine combines rule-style signals and beneficiary/behavioral data.
The result is persisted as a transaction. Scores at or above the configured
high-risk threshold are initially marked `BLOCKED` in the simulation.

Invoice analysis:

- validates file type and maximum size;
- extracts text from the uploaded demo-compatible input;
- compares the extracted account and IFSC with registered vendor values;
- calculates mismatch flags, score, risk level, reasons, and recommended action;
- persists an invoice record.

Rescue:

- validates the transaction ID;
- marks the transaction as fraud reported;
- creates a fraud incident;
- calls the simulated bank-freeze service;
- creates a freeze request;
- generates a SHA-256-associated evidence report;
- marks recovery as initiated.

### Backend local setup

```powershell
cd D:\FinSentry-360\Backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

For local SQLite development, use:

```env
DATABASE_URL=sqlite:///./finsentry.db
DEMO_COOLDOWN_SECONDS=10
MAX_INVOICE_BYTES=5242880
CORS_ORIGINS=http://localhost:5173
```

Seed demo data:

```powershell
python -m app.seed.seed_database
```

Run the API:

```powershell
uvicorn app.main:app --reload
```

API documentation is available at `http://localhost:8000/docs`.

## Frontend

### Technology

- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios
- React Flow
- Lucide icons
- Recharts dependency
- Vitest

### Frontend screens

Routes currently include:

| Route | Purpose |
|---|---|
| `/` | Executive dashboard |
| `/payment-guard` | Payment risk analysis and confirmation |
| `/corporate-guard` | Invoice analysis and blocking |
| `/rescue` | Golden-hour rescue workflow |
| `/transactions` | Persisted transaction list |
| `/incidents` | Persisted fraud incident list |
| `/network` | Beneficiary relationship graph |
| `/settings` | Prototype settings/information screen |

### Frontend local setup

```powershell
cd D:\FinSentry-360\Frontend
npm ci
copy .env.example .env
```

Use:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCK_API=false
```

Run the development server:

```powershell
npm run dev
```

For a self-contained UI demo without the backend:

```env
VITE_USE_MOCK_API=true
```

The UI labels mock actions as simulated. Mock mode is not a replacement for
backend integration testing.

## Data model

The SQLAlchemy models currently include:

- `User` - demo user/customer identity.
- `Beneficiary` - recipient account, bank, risk, complaint, velocity, and
  known-mule attributes.
- `Transaction` - amount, recipient, behavioral signals, risk result, status,
  and timestamps.
- `FraudIncident` - incident reference, transaction, fraud type, score,
  description, and recovery state.
- `FreezeRequest` - simulated bank-freeze request and response.
- `Invoice` - vendor/invoice values, mismatch flags, score, level, and status.
- `EvidenceReport` - report path, hash, incident, and generation status.

Tables are created at application startup with SQLAlchemy metadata. The seed
script creates demo users, beneficiaries, and transactions.

## Main user workflows

### Payment risk

1. Enter an amount and beneficiary ID.
2. Enter optional behavioral/session signals.
3. The frontend calls `POST /api/v1/risk/analyze-transaction`.
4. The backend validates the beneficiary and stores the transaction.
5. The UI shows score, level, reasons, and recommended action.
6. Confirmation calls `POST /api/v1/transactions/{id}/confirm`.

### Invoice protection

1. Upload a supported demo invoice file.
2. The frontend sends multipart data to `POST /api/v1/invoices/analyze`.
3. The backend persists the invoice analysis.
4. The user can call `POST /api/v1/invoices/{id}/block`.

### Fraud rescue

1. Start from a real transaction ID generated by payment analysis.
2. Submit a description to `POST /api/v1/rescue/sos`.
3. The backend creates an incident, freeze request, and evidence report.
4. The UI displays the simulated recovery result and report hash.

## Configuration

### Backend variables

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLAlchemy database URL |
| `CORS_ORIGINS` | Comma-separated frontend origins |
| `DEMO_COOLDOWN_SECONDS` | Demo cooldown shown for high-risk payments |
| `MAX_INVOICE_BYTES` | Maximum accepted invoice upload size |

For Supabase/PostgreSQL, use a SQLAlchemy URL such as:

```env
DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@HOST:PORT/postgres?sslmode=require
```

URL-encode special characters in the password. Never commit the real `.env`
file. Rotate any database credential that has been exposed.

### Frontend variables

| Variable | Purpose |
|---|---|
| `VITE_API_BASE_URL` | Backend origin used by Axios |
| `VITE_USE_MOCK_API` | Enables frontend-only demo responses |
| `NEXT_PUBLIC_SUPABASE_URL` | Reserved Supabase project setting |
| `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` | Reserved public Supabase key |

The current application persists through the FastAPI backend; the frontend
does not directly query Supabase.

## Testing

Backend syntax and tests:

```powershell
cd D:\FinSentry-360\Backend
python -m compileall app
pytest -q
```

Frontend:

```powershell
cd D:\FinSentry-360\Frontend
npm test
npm run build
```

## Render deployment

Deploy the services separately from the same repository.

### Backend Web Service

| Render setting | Value |
|---|---|
| Root Directory | `Backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

Set `DATABASE_URL`, `CORS_ORIGINS`, `DEMO_COOLDOWN_SECONDS`, and
`MAX_INVOICE_BYTES` in Render's environment settings.

### Frontend Static Site

| Render setting | Value |
|---|---|
| Root Directory | `Frontend` |
| Build Command | `npm ci && npm run build` |
| Publish Directory | `dist` |

Set:

```env
VITE_API_BASE_URL=https://your-backend.onrender.com
VITE_USE_MOCK_API=false
```

Add a Render rewrite from `/*` to `/index.html` so browser refreshes work on
React Router routes. After the frontend URL is known, set backend
`CORS_ORIGINS` to that exact URL and redeploy the backend.

## API reference

All routes below are prefixed with `/api/v1`.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Service health and simulation status |
| `POST` | `/risk/analyze-transaction` | Score and persist a transaction |
| `POST` | `/risk/explain` | Return risk analysis |
| `POST` | `/transactions/{id}/confirm` | Confirm a transaction |
| `GET` | `/beneficiaries/{id}` | Validate beneficiary ID |
| `GET` | `/beneficiaries/{id}/network` | Build beneficiary network |
| `POST` | `/invoices/analyze` | Analyze uploaded invoice |
| `POST` | `/invoices/{id}/block` | Mark invoice as blocked |
| `POST` | `/rescue/sos` | Start simulated rescue workflow |
| `POST` | `/reports/generate/{id}` | Generate incident evidence |
| `POST` | `/mock-bank/freeze` | Run simulated bank freeze |
| `GET` | `/dashboard/summary` | Dashboard totals |
| `GET` | `/dashboard/recent-incidents` | Recent incidents |
| `GET` | `/dashboard/risk-distribution` | Risk-level counts |
| `GET` | `/dashboard/activity` | Recent transaction activity |
| `GET` | `/transactions` | Transaction list |
| `GET` | `/incidents` | Incident list |

## Security and operational limitations

This prototype intentionally does not yet provide:

- authentication or authorization;
- tenant isolation;
- audit-grade immutable event storage;
- production OCR accuracy guarantees;
- real payment or bank integrations;
- real account freezing;
- production fraud-model governance;
- rate limiting or abuse prevention;
- secrets management beyond host environment variables;
- database migrations;
- durable object storage for generated reports;
- complete compliance controls and legal review;
- observability, alerting, and incident response operations.

The generated reports are demo evidence artifacts, not legal filings. Do not
use prototype scores as an automatic real-world payment decision.

## Roadmap

### Near term

- Add automated API and browser end-to-end coverage.
- Add structured application logging and request IDs.
- Add database migrations with Alembic.
- Add environment validation at startup.
- Add durable report storage.
- Improve invoice parsing and OCR fixtures.

### Production-readiness phase

- Add identity, role-based access, and organization isolation.
- Replace simulated actions with approved provider integrations behind adapters.
- Add model evaluation, threshold governance, explainability, and drift checks.
- Add idempotency, retries, queues, and rate limits.
- Add encrypted secrets and managed identity where supported.
- Add backups, monitoring, alerting, and disaster recovery.
- Complete security testing, privacy review, legal review, and compliance
  certification.
