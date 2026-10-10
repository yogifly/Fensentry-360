from app.utils.risk import level
def assess_beneficiary(b):
    score=0; signals=[]
    if b.account_age_days<30: score+=25; signals.append("Beneficiary account is recently created")
    if b.complaint_count: 
        score += 15 if b.complaint_count<=2 else 30 if b.complaint_count<=5 else 40
        signals.append(f"{b.complaint_count} complaints recorded")
    if b.transaction_velocity>=20: score+=20; signals.append("High transaction velocity")
    if b.is_known_mule: score+=40; signals.append("Beneficiary is marked as a known mule")
    return {"beneficiary_score":min(score,100),"risk_level":level(score),"signals":signals}
