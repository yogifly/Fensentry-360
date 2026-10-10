from app.services.behavioral_engine import assess_behavior
from app.services.invoice_engine import analyze_text
def test_behavior_high(): assert assess_behavior({"active_call":True,"screen_sharing":True,"typing_deviation":.8,"touch_jitter":.8})["behavioral_score"]>=80
def test_invoice_mismatch(): assert analyze_text("Account 9876543210 IFSC HDFC0005678", "1234567890","HDFC0001234")["risk_level"]=="CRITICAL"
