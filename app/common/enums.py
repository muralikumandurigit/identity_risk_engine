from enum import Enum

class IntentType(str, Enum):
    ACCESS_INVESTIGATION = "access_investigation"
    RISK_ANALYSIS = "risk_analysis"
    AUDIT = "audit"
    POLICY_SIMULATION = "policy_simulation"
