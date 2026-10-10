import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'finsentry.db'}")
DEMO_COOLDOWN_SECONDS = int(os.getenv("DEMO_COOLDOWN_SECONDS", "10"))
MAX_INVOICE_BYTES = int(os.getenv("MAX_INVOICE_BYTES", "5242880"))
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "*").split(",")
    if origin.strip()
]
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)
SIMULATION_LABEL = "DEMO / SIMULATION ONLY"
