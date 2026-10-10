from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True); name=Column(String,nullable=False); email=Column(String,unique=True); phone=Column(String); user_type=Column(String,default="CONSUMER"); created_at=Column(DateTime,default=datetime.utcnow)
class Beneficiary(Base):
    __tablename__="beneficiaries"
    id=Column(Integer,primary_key=True); name=Column(String,nullable=False); account_number_masked=Column(String); bank_name=Column(String); ifsc=Column(String); account_age_days=Column(Integer,default=365); complaint_count=Column(Integer,default=0); transaction_velocity=Column(Integer,default=0); risk_score=Column(Float,default=0); risk_level=Column(String,default="LOW"); is_known_mule=Column(Boolean,default=False); created_at=Column(DateTime,default=datetime.utcnow)
class Transaction(Base):
    __tablename__="transactions"
    id=Column(Integer,primary_key=True); transaction_reference=Column(String,unique=True); user_id=Column(Integer,ForeignKey("users.id")); beneficiary_id=Column(Integer,ForeignKey("beneficiaries.id")); amount=Column(Float); transaction_type=Column(String,default="UPI_SIMULATION"); device_id=Column(String); ip_address=Column(String)
    active_call=Column(Boolean,default=False); screen_sharing=Column(Boolean,default=False); typing_deviation=Column(Float,default=0); touch_jitter=Column(Float,default=0); touch_pressure=Column(Float,default=0); session_duration=Column(Float,default=0); amount_anomaly=Column(Float,default=0); transaction_velocity=Column(Float,default=0); beneficiary_age_days=Column(Integer,default=365); beneficiary_complaints=Column(Integer,default=0); risk_score=Column(Float,default=0); risk_level=Column(String,default="LOW"); risk_reasons=Column(Text,default="[]"); status=Column(String,default="PENDING"); created_at=Column(DateTime,default=datetime.utcnow); updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    beneficiary=relationship("Beneficiary"); user=relationship("User")
class FraudIncident(Base):
    __tablename__="fraud_incidents"
    id=Column(Integer,primary_key=True); incident_reference=Column(String,unique=True); transaction_id=Column(Integer,ForeignKey("transactions.id")); fraud_type=Column(String,default="UNKNOWN"); description=Column(Text); fraud_score=Column(Float); reported_at=Column(DateTime,default=datetime.utcnow); status=Column(String,default="OPEN"); recovery_status=Column(String,default="INITIATED"); created_at=Column(DateTime,default=datetime.utcnow); transaction=relationship("Transaction")
class FreezeRequest(Base):
    __tablename__="freeze_requests"
    id=Column(Integer,primary_key=True); incident_id=Column(Integer,ForeignKey("fraud_incidents.id")); bank_name=Column(String); recipient_account=Column(String); request_type=Column(String,default="MOCK_BANK_FREEZE"); status=Column(String); requested_at=Column(DateTime,default=datetime.utcnow); processed_at=Column(DateTime); response_message=Column(Text)
class Invoice(Base):
    __tablename__="invoices"
    id=Column(Integer,primary_key=True); vendor_name=Column(String); invoice_number=Column(String); invoice_amount=Column(Float); invoice_account=Column(String); invoice_ifsc=Column(String); expected_account=Column(String); expected_ifsc=Column(String); ocr_confidence=Column(Float,default=0); metadata_anomaly=Column(Boolean,default=False); account_mismatch=Column(Boolean,default=False); ifsc_mismatch=Column(Boolean,default=False); layout_anomaly=Column(Boolean,default=False); risk_score=Column(Float,default=0); risk_level=Column(String,default="LOW"); status=Column(String,default="ANALYZED"); created_at=Column(DateTime,default=datetime.utcnow)
class EvidenceReport(Base):
    __tablename__="evidence_reports"
    id=Column(Integer,primary_key=True); incident_id=Column(Integer,ForeignKey("fraud_incidents.id")); report_path=Column(String); sha256_hash=Column(String); generated_at=Column(DateTime,default=datetime.utcnow); report_status=Column(String,default="GENERATED")
