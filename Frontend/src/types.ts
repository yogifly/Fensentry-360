export type RiskLevel='LOW'|'MEDIUM'|'HIGH'|'CRITICAL';
export interface RiskResult { risk_score:number; risk_probability:number; risk_level:RiskLevel; recommended_action:string; reasons:string[]; transaction_id:number; cooldown_required:boolean; cooldown_seconds:number; behavioral?:{behavioral_score:number;signals:string[]}; beneficiary?:{beneficiary_score:number;signals:string[]}; simulation?:boolean }
export interface Dashboard { total_transactions:number; blocked_transactions:number; high_risk_transactions:number; fraud_incidents:number; recovered_frozen_amount:number; invoices_analyzed:number; critical_invoices:number }
export interface Incident { id:number; reference:string; status:string; score:number; created_at:string; fraud_type?:string }
export interface InvoiceResult { id:number; invoice_account:string; invoice_ifsc:string; invoice_amount:number; account_mismatch:boolean; ifsc_mismatch:boolean; risk_score:number; risk_level:RiskLevel; reasons:string[]; recommended_action:string; simulation?:boolean }
export interface Network { simulation:boolean; nodes:{id:string;label:string;type:string;risk_level:string}[]; edges:{source:string;target:string;relation:string}[] }
export interface Beneficiary { id:number; name:string; bank_name:string; account_number_masked:string; risk_level:RiskLevel; is_known_mule:boolean }
export interface ActivityPoint { id:number; status:string; amount:number; created_at:string }
export interface Transaction { id:number; reference:string; amount:number; beneficiary_id:number; risk_score:number; risk_level:RiskLevel; status:string; created_at:string }
export interface IncidentRecord { id:number; reference:string; transaction_id:number; fraud_type:string; score:number; status:string; recovery_status:string; description:string; created_at:string }
export type RiskDistribution = Record<RiskLevel, number>;
