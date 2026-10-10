from app.utils.risk import level
def assess_behavior(data):
    score=0; signals=[]
    if data.get("active_call"): score+=22; signals.append("Active call detected (demo sensor simulation)")
    if data.get("screen_sharing"): score+=25; signals.append("Screen sharing detected (demo sensor simulation)")
    if data.get("typing_deviation",0)>=.7: score+=20; signals.append("High typing deviation")
    if data.get("touch_jitter",0)>=.65: score+=18; signals.append("Elevated touch jitter")
    if data.get("touch_pressure",0)>=.7: score+=8; signals.append("Unusual touch pressure")
    if data.get("session_duration",0)>30: score+=7; signals.append("Extended transaction session")
    return {"behavioral_score":min(score,100),"risk_level":level(score),"signals":signals}
