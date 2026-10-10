from typing import Optional
from pydantic import BaseModel, Field
class RiskRequest(BaseModel):
    amount: float = Field(gt=0); beneficiary_id: int
    active_call: bool=False; screen_sharing: bool=False; typing_deviation: float=Field(0,ge=0,le=1); touch_jitter: float=Field(0,ge=0,le=1); touch_pressure: float=Field(0,ge=0,le=1); session_duration: float=Field(0,ge=0); amount_anomaly: float=Field(0,ge=0,le=1); transaction_velocity: float=Field(0,ge=0)
class ConfirmRequest(BaseModel): override_warning: bool=False
class SosRequest(BaseModel): transaction_id: int; description: str
