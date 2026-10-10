import re
from app.utils.risk import level
def analyze_text(text, expected_account=None, expected_ifsc=None):
    account=(re.search(r"(?:account|a/c)[^\d]*(\d{6,})",text,re.I) or [None,""])[1]
    ifsc=(re.search(r"\b([A-Z]{4}0[A-Z0-9]{6})\b",text,re.I) or [None,""])[1].upper()
    amount=float((re.search(r"(?:amount|total)[^\d]*(\d+(?:\.\d+)?)",text,re.I) or [None,0])[1])
    am=bool(expected_account and account and account!=expected_account); im=bool(expected_ifsc and ifsc and ifsc!=expected_ifsc)
    score=min(100,(45 if am else 0)+(35 if im else 0)+(20 if not account or not ifsc else 0)); reasons=[]
    if am: reasons.append("Bank account does not match registered vendor account")
    if im: reasons.append("IFSC does not match registered vendor IFSC")
    return {"invoice_account":account,"invoice_ifsc":ifsc,"invoice_amount":amount,"account_mismatch":am,"ifsc_mismatch":im,"risk_score":score,"risk_level":level(score),"reasons":reasons,"recommended_action":"BLOCK_PAYMENT" if score>=80 else "REVIEW"}
