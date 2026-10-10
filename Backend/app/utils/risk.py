from app.config.constants import risk_level
def level(score): return risk_level(max(0,min(100,round(score)))).value
