# FinSentry 360 frontend

React + TypeScript + Vite + Tailwind MVP for the FastAPI service in `Backend`.

```bash
npm install
copy .env.example .env
npm run dev
```

Set `VITE_API_BASE_URL` to the FastAPI origin. Set `VITE_USE_MOCK_API=true` explicitly for the self-contained simulation (the UI labels all simulated actions). API calls match the routes in `Backend/app/api/routes.py`: dashboard summary/incidents, transaction risk analysis/confirmation, invoice analysis, rescue SOS, and beneficiary network.
