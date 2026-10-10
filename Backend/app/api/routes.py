import json, uuid
from datetime import datetime
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models import *
from app.schemas.api import *
from app.services.risk_engine import analyze
from app.services.graph_engine import build_network
from app.services.mock_bank import freeze_account
from app.services.evidence_engine import generate_report
from app.services.invoice_engine import analyze_text
from app.config.settings import DEMO_COOLDOWN_SECONDS, MAX_INVOICE_BYTES, SIMULATION_LABEL
router=APIRouter(prefix="/api/v1")
def err(code,msg): raise HTTPException(400,{"success":False,"error_code":code,"message":msg})
@router.get("/health")
def health(): return {"status":"ok","simulation":True,"label":SIMULATION_LABEL}
@router.post("/risk/analyze-transaction")
def risk(req:RiskRequest,db:Session=Depends(get_db)):
    b=db.get(Beneficiary,req.beneficiary_id)
    if not b: err("INVALID_BENEFICIARY","Beneficiary not found")
    result=analyze(req.amount,b,req.model_dump()); values={k:v for k,v in req.model_dump().items() if k in Transaction.__table__.columns.keys() and k not in ("amount","beneficiary_id")}; t=Transaction(transaction_reference="TX-"+uuid.uuid4().hex[:10].upper(),beneficiary_id=b.id,amount=req.amount,**values); t.risk_score=result["risk_score"]; t.risk_level=result["risk_level"]; t.risk_reasons=json.dumps(result["reasons"]); t.status="BLOCKED" if t.risk_score>=80 else "APPROVED"; db.add(t); db.commit(); db.refresh(t)
    result.update({"transaction_id":t.id,"cooldown_required":t.risk_score>=80,"cooldown_seconds":DEMO_COOLDOWN_SECONDS if t.risk_score>=80 else 0,"production_cooldown_seconds":60,"simulation":True}); return result
@router.post("/risk/explain")
def explain(req:RiskRequest,db:Session=Depends(get_db)):
    return risk(req,db)
@router.post("/transactions/{transaction_id}/confirm")
def confirm(transaction_id:int, req:ConfirmRequest,db:Session=Depends(get_db)):
    t=db.get(Transaction,transaction_id)
    if not t: err("INVALID_TRANSACTION","Transaction not found")
    if t.status=="BLOCKED" and not req.override_warning: return {"success":False,"cooldown_required":True,"message":"Explicit demo override required","transaction_id":t.id}
    t.status="COMPLETED"; db.commit(); return {"success":True,"transaction_id":t.id,"status":t.status,"simulation":True}
@router.get("/beneficiaries/{beneficiary_id}/network")
def network(beneficiary_id:int,db:Session=Depends(get_db)):
    b=db.get(Beneficiary,beneficiary_id)
    if not b: err("INVALID_BENEFICIARY","Beneficiary not found")
    u=db.query(User).first() or User(id=0,name="Demo Victim"); return build_network(u,b)
@router.get("/beneficiaries/{beneficiary_id}")
def beneficiary(beneficiary_id:int,db:Session=Depends(get_db)):
    b=db.get(Beneficiary,beneficiary_id)
    if not b: err("INVALID_BENEFICIARY","Beneficiary ID not found")
    return {"id":b.id,"name":b.name,"bank_name":b.bank_name,"account_number_masked":b.account_number_masked,"risk_level":b.risk_level,"is_known_mule":b.is_known_mule,"simulation":True}
@router.post("/invoices/analyze")
async def invoice(file:UploadFile=File(...),db:Session=Depends(get_db)):
    if file.content_type not in ("application/pdf","text/plain"): err("INVALID_FILE_TYPE","Only PDF uploads are accepted")
    body=await file.read()
    if len(body)>MAX_INVOICE_BYTES: err("FILE_TOO_LARGE","Invoice exceeds upload limit")
    text=body.decode("utf-8","ignore"); result=analyze_text(text, expected_account="1234567890", expected_ifsc="HDFC0001234")
    inv=Invoice(**{k:v for k,v in result.items() if k in Invoice.__table__.columns.keys()}); db.add(inv); db.commit(); db.refresh(inv); return {"id":inv.id,**result,"simulation":True}
@router.post("/invoices/{invoice_id}/block")
def block_invoice(invoice_id:int,db:Session=Depends(get_db)):
    inv=db.get(Invoice,invoice_id)
    if not inv: err("INVALID_INVOICE","Invoice not found")
    inv.status="BLOCKED"; db.commit()
    return {"success":True,"invoice_id":inv.id,"status":inv.status,"simulation":True}
@router.post("/rescue/sos")
def sos(req:SosRequest,db:Session=Depends(get_db)):
    t=db.get(Transaction,req.transaction_id)
    if not t: err("INVALID_TRANSACTION","Transaction not found")
    t.status="FRAUD_REPORTED"; i=FraudIncident(incident_reference="INC-"+uuid.uuid4().hex[:10].upper(),transaction_id=t.id,description=req.description,fraud_score=t.risk_score or 80,fraud_type="SOCIAL_ENGINEERING"); db.add(i); db.commit(); db.refresh(i)
    freeze=freeze_account(t.beneficiary.bank_name if t.beneficiary else "Demo Bank",t.beneficiary.account_number_masked if t.beneficiary else "0000"); fr=FreezeRequest(incident_id=i.id,bank_name=freeze["bank"],recipient_account=freeze["recipient_account"],status=freeze["status"],processed_at=datetime.utcnow(),response_message=freeze["message"]); db.add(fr); db.commit()
    path,digest=generate_report(i,t,t.beneficiary,freeze); er=EvidenceReport(incident_id=i.id,report_path=path,sha256_hash=digest); db.add(er); i.recovery_status="INITIATED"; db.commit()
    return {"incident_id":i.id,"transaction_locked":True,"freeze_request":freeze,"evidence_report":{"status":"GENERATED","sha256_hash":digest,"report_path":path},"recovery_status":i.recovery_status,"simulation":True}
@router.post("/reports/generate/{incident_id}")
def report(incident_id:int,db:Session=Depends(get_db)):
    i=db.get(FraudIncident,incident_id)
    if not i: err("INVALID_INCIDENT","Incident not found")
    if i.transaction is None: err("INVALID_TRANSACTION","Transaction unavailable")
    freeze={"status":"ACCEPTED","bank":"Demo Bank","recipient_account":"****"}
    path,digest=generate_report(i,i.transaction,i.transaction.beneficiary,freeze); return {"status":"GENERATED","path":path,"sha256_hash":digest,"simulation":True}
@router.post("/mock-bank/freeze")
def mock_freeze(bank_name:str="Demo Bank",recipient_account:str="0000"): return freeze_account(bank_name,recipient_account)
@router.get("/dashboard/summary")
def summary(db:Session=Depends(get_db)):
    ts=db.query(Transaction).all(); inv=db.query(Invoice).all(); return {"total_transactions":len(ts),"blocked_transactions":sum(t.status=="BLOCKED" for t in ts),"high_risk_transactions":sum(t.risk_score>=60 for t in ts),"fraud_incidents":db.query(FraudIncident).count(),"recovered_frozen_amount":sum(t.amount for t in ts if t.status in ("FROZEN","FRAUD_REPORTED")),"invoices_analyzed":len(inv),"critical_invoices":sum(i.risk_score>=80 for i in inv)}
@router.get("/dashboard/recent-incidents")
def recent(db:Session=Depends(get_db)): return [{"id":i.id,"reference":i.incident_reference,"status":i.status,"score":i.fraud_score,"created_at":i.created_at} for i in db.query(FraudIncident).order_by(FraudIncident.created_at.desc()).limit(20)]
@router.get("/dashboard/risk-distribution")
def distribution(db:Session=Depends(get_db)): return {x:db.query(Transaction).filter(Transaction.risk_level==x).count() for x in ("LOW","MEDIUM","HIGH","CRITICAL")}
@router.get("/dashboard/activity")
def activity(db:Session=Depends(get_db)): return [{"id":t.id,"status":t.status,"amount":t.amount,"created_at":t.created_at} for t in db.query(Transaction).order_by(Transaction.created_at.desc()).limit(50)]
@router.get("/transactions")
def transactions(db:Session=Depends(get_db)):
    return [{"id":t.id,"reference":t.transaction_reference,"amount":t.amount,"beneficiary_id":t.beneficiary_id,"risk_score":t.risk_score,"risk_level":t.risk_level,"status":t.status,"created_at":t.created_at} for t in db.query(Transaction).order_by(Transaction.created_at.desc()).limit(100)]
@router.get("/incidents")
def incidents(db:Session=Depends(get_db)):
    return [{"id":i.id,"reference":i.incident_reference,"transaction_id":i.transaction_id,"fraud_type":i.fraud_type,"score":i.fraud_score,"status":i.status,"recovery_status":i.recovery_status,"description":i.description,"created_at":i.created_at} for i in db.query(FraudIncident).order_by(FraudIncident.created_at.desc()).limit(100)]
