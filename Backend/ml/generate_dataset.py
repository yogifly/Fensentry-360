from pathlib import Path
import numpy as np,pandas as pd
def main(n=20000):
    rng=np.random.default_rng(42); d=pd.DataFrame({k:rng.random(n) for k in ["typing_deviation","touch_jitter","touch_pressure","amount_anomaly"]}); d["amount"]=rng.lognormal(8,1,n); d["account_age_days"]=rng.integers(1,1000,n); d["complaint_count"]=rng.poisson(1,n); d["transaction_velocity"]=rng.integers(0,40,n); d["active_call"]=rng.integers(0,2,n); d["screen_sharing"]=rng.integers(0,2,n); d["session_duration"]=rng.integers(1,100,n); d["previous_transactions"]=rng.integers(0,100,n); d["is_known_mule"]=rng.integers(0,2,n); p=(d.amount>50000)*.2+(d.account_age_days<30)*.2+d.active_call*.15+d.screen_sharing*.2+d.is_known_mule*.3+d.typing_deviation*.1; d["fraud"]=(rng.random(n)<np.clip(p,.02,.95)).astype(int); out=Path(__file__).parents[2]/"data/generated/transactions.csv"; out.parent.mkdir(exist_ok=True,parents=True); d.to_csv(out,index=False)
if __name__=="__main__": main()
