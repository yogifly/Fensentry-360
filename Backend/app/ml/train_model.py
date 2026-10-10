"""Train and persist the optional fraud model from the synthetic dataset."""
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def train():
    root=Path(__file__).parents[2]; data=pd.read_csv(root/"data/generated/transactions.csv")
    x=data.drop(columns=["fraud"]); y=data["fraud"]; xt,xv,yt,yv=train_test_split(x,y,test_size=.2,random_state=42,stratify=y)
    model=RandomForestClassifier(n_estimators=100,random_state=42,n_jobs=-1).fit(xt,yt)
    p=model.predict(xv); proba=model.predict_proba(xv)[:,1]
    metrics={"accuracy":accuracy_score(yv,p),"precision":precision_score(yv,p,zero_division=0),"recall":recall_score(yv,p,zero_division=0),"f1":f1_score(yv,p,zero_division=0),"roc_auc":roc_auc_score(yv,proba)}
    out=Path(__file__).parent/"model"; out.mkdir(exist_ok=True); joblib.dump(model,out/"fraud_model.pkl"); (out/"feature_names.json").write_text(json.dumps(list(x.columns),indent=2)); return metrics
if __name__=="__main__": print(train())
