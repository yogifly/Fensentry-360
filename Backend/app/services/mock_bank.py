from datetime import datetime
def freeze_account(bank_name, account):
    return {"simulation":True,"status":"ACCEPTED","bank":bank_name or "Demo Bank","recipient_account":"****"+str(account)[-4:],"message":"Demo bank has frozen the recipient account","processed_at":datetime.utcnow().isoformat()}
def get_account_status(account): return {"simulation":True,"account":"****"+str(account)[-4:],"status":"FROZEN"}
def send_fraud_alert(account, description): return {"simulation":True,"status":"SENT","message":"Demo fraud alert sent"}
