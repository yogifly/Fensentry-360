from app.database.database import Base,engine,SessionLocal
from app.database.models import User,Beneficiary,Transaction,FraudIncident
Base.metadata.create_all(bind=engine)
db=SessionLocal()
if not db.query(User).count():
    db.add_all([User(name=f"Demo User {i}",email=f"user{i}@demo.local",phone="0000000000") for i in range(1,11)])
    db.add_all([Beneficiary(name=f"Demo Beneficiary {i}",account_number_masked=f"****{1000+i}",bank_name="Demo HDFC Bank",ifsc="HDFC0001234",account_age_days=3 if i==2 else 500,complaint_count=4 if i==2 else 0,transaction_velocity=30 if i==2 else 3,is_known_mule=i==3,risk_level="CRITICAL" if i in (2,3) else "LOW") for i in range(1,16)])
    db.commit()
if not db.query(Transaction).count():
    users=db.query(User).all()
    beneficiaries=db.query(Beneficiary).all()
    transactions=[]
    for i in range(30):
        beneficiary=beneficiaries[i % len(beneficiaries)]
        high_risk=beneficiary.id in (2,3) or i % 7 == 0
        transactions.append(Transaction(
            transaction_reference=f"SEED-TX-{i+1:04d}",
            user_id=users[i % len(users)].id,
            beneficiary_id=beneficiary.id,
            amount=75000 if high_risk else 2000 + i * 125,
            active_call=high_risk,
            screen_sharing=high_risk,
            typing_deviation=0.85 if high_risk else 0.1,
            touch_jitter=0.8 if high_risk else 0.08,
            touch_pressure=0.7 if high_risk else 0.1,
            session_duration=45 if high_risk else 120,
            amount_anomaly=0.7 if high_risk else 0.05,
            transaction_velocity=25 if high_risk else 2,
            risk_score=92 if high_risk else 8,
            risk_level="CRITICAL" if high_risk else "LOW",
            risk_reasons='["Seeded demo risk scenario"]' if high_risk else '[]',
            status="BLOCKED" if high_risk else "APPROVED",
        ))
    db.add_all(transactions)
    db.commit()
db.close()
