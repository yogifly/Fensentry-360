# FinSentry 360 MVP

FinSentry 360 is a FastAPI prototype for pre-execution fraud scoring and golden-hour recovery. **Every payment, bank freeze, graph relationship, and law-enforcement report is simulated; this system must not be connected to real financial infrastructure.**

## Run locally

```powershell
cd Backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL="sqlite:///./finsentry.db"
python -m app.seed.seed_database
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs`. PostgreSQL is supported by setting `DATABASE_URL` to a SQLAlchemy PostgreSQL URL. `docker compose up --build` starts PostgreSQL and the API.

## Deploy to Render

Create a Render Web Service for `Backend` with:

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment variables: `DATABASE_URL`, `CORS_ORIGINS`, `DEMO_COOLDOWN_SECONDS`, and `MAX_INVOICE_BYTES`

Set `CORS_ORIGINS` to the deployed frontend URL, for example
`https://finsentry-360-frontend.onrender.com`. Do not commit `.env`; enter secrets in
Render's Environment settings.

## APIs

- `POST /api/v1/risk/analyze-transaction` hybrid beneficiary, behavioral, rules and model-style score
- `POST /api/v1/risk/explain`
- `POST /api/v1/transactions/{id}/confirm`
- `GET /api/v1/beneficiaries/{id}/network`
- `POST /api/v1/invoices/analyze` (PDF or text-compatible demo fixture, size/type validated)
- `POST /api/v1/rescue/sos`
- `POST /api/v1/reports/generate/{incident_id}`
- `POST /api/v1/mock-bank/freeze`
- dashboard summary, incidents, distribution and activity endpoints

## Dataset and testing

`python ml/generate_dataset.py` creates 20,000 noisy synthetic records under `data/generated`. Train a production model only after adding a reviewed `train_model.py`; no model is used as the sole decision maker. Run `pytest` from `Backend`.

Example:

```powershell
curl -X POST http://localhost:8000/api/v1/risk/analyze-transaction -H "Content-Type: application/json" -d '{"amount":50000,"beneficiary_id":2,"active_call":true,"screen_sharing":true,"typing_deviation":0.82,"touch_jitter":0.76,"touch_pressure":0.7,"session_duration":45}'
curl -X POST http://localhost:8000/api/v1/rescue/sos -H "Content-Type: application/json" -d '{"transaction_id":1,"description":"Demo social engineering incident"}'
```

Reports are generated in `reports/` with a SHA-256 hash and disclaimer `DEMO/SIMULATION REPORT — NOT A LEGAL FIR`. Sensitive account values are masked. This MVP intentionally omits authentication, real OCR infrastructure, real banking/payment integrations, and production compliance controls.
