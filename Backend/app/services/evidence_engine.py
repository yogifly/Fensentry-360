import hashlib
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.config.settings import REPORT_DIR, SIMULATION_LABEL
def generate_report(incident, transaction, beneficiary, freeze):
    path=REPORT_DIR/f"incident-{incident.id}.pdf"; c=canvas.Canvas(str(path),pagesize=letter); y=760
    lines=["FINSentry 360","CYBER FRAUD INCIDENT REPORT",SIMULATION_LABEL,f"Incident: {incident.incident_reference}",f"Transaction: {transaction.transaction_reference}",f"Amount: {transaction.amount}",f"Victim: {transaction.user.name if transaction.user else 'Demo User'}",f"Recipient: {beneficiary.name}",f"Fraud type: {incident.fraud_type}",f"Fraud score: {incident.fraud_score}",f"Risk reasons: {transaction.risk_reasons}",f"Freeze: {freeze.get('status')}",f"Recovery: {incident.recovery_status}","DISCLAIMER: DEMO/SIMULATION REPORT — NOT A LEGAL FIR"]
    for line in lines: c.drawString(50,y,line[:110]); y-=22
    c.save(); digest=hashlib.sha256(path.read_bytes()).hexdigest(); return str(path),digest
