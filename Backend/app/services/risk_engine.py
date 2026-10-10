import json
from app.services.behavioral_engine import assess_behavior
from app.services.beneficiary_engine import assess_beneficiary
def analyze(amount, beneficiary, payload):
    b=assess_beneficiary(beneficiary); beh=assess_behavior(payload)
    rules=min(100, amount/1000 + payload.get("amount_anomaly",0)*20 + (20 if payload.get("transaction_velocity",0)>20 else 0))
    ml=min(1, .05 + rules/200 + beh["behavioral_score"]/250 + b["beneficiary_score"]/250)
    score=min(100, round(ml*45 + b["beneficiary_score"]*.3 + beh["behavioral_score"]*.25 + rules*.1))
    reasons=b["signals"]+beh["signals"]
    if amount>30000: reasons.append("High transaction amount")
    if payload.get("amount_anomaly",0)>.5: reasons.append("Amount differs from normal behavior")
    level="CRITICAL" if score>=80 else "HIGH" if score>=60 else "MEDIUM" if score>=30 else "LOW"
    return {"risk_score":score,"risk_probability":round(score/100,2),"risk_level":level,"recommended_action":"BLOCK" if score>=80 else "REVIEW" if score>=60 else "APPROVE","reasons":reasons,"behavioral":beh,"beneficiary":b}
