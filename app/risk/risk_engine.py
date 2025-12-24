from typing import Dict, List

def compute_identity_risk(
    auth_context: Dict,
    access_context: Dict
) -> Dict:
    """
    Deterministic identity risk scoring.
    """
    risk_score = 0.0
    factors: List[str] = []

    roles = access_context.get("roles", [])

    # --- SoD violations ---
    if "prod_db_admin" in roles and "finance_viewer" in roles:
        risk_score += 0.4
        factors.append(
            "Segregation of Duties violation: prod_db_admin + finance_viewer"
        )

    # --- Authentication risk signals ---
    if auth_context.get("anomalous_login"):
        risk_score += 0.2
        factors.append("Anomalous login detected")

    if not auth_context.get("device_trusted"):
        risk_score += 0.2
        factors.append("Access from untrusted device")

    if not auth_context.get("mfa"):
        risk_score += 0.2
        factors.append("MFA not enabled")

    risk_score = min(risk_score, 1.0)

    if risk_score >= 0.7:
        level = "HIGH"
    elif risk_score >= 0.4:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": round(risk_score, 2),
        "risk_level": level,
        "factors": factors
    }
