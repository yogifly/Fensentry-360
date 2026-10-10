from enum import Enum

class RiskLevel(str, Enum):
    LOW = "LOW"; MEDIUM = "MEDIUM"; HIGH = "HIGH"; CRITICAL = "CRITICAL"
class TransactionStatus(str, Enum):
    PENDING = "PENDING"; APPROVED = "APPROVED"; BLOCKED = "BLOCKED"; COMPLETED = "COMPLETED"; FRAUD_REPORTED = "FRAUD_REPORTED"; FROZEN = "FROZEN"
def risk_level(score: float) -> RiskLevel:
    return RiskLevel.CRITICAL if score >= 80 else RiskLevel.HIGH if score >= 60 else RiskLevel.MEDIUM if score >= 30 else RiskLevel.LOW
