import re
from app.common.enums import IntentType

def classify_intent_and_entity(query: str) -> IntentType:
    q = query.lower()

    # Very simple user extraction (we’ll improve later)
    user_match = re.search(r"\b(bob|alice)\b", q)
    subject_user = user_match.group(1) if user_match else None

    # extract role
    role_match = re.search(r"remove\s+([a-zA-Z0-9_]+)", q)
    role = role_match.group(1) if role_match else None

    if "why" in q and "access" in q:
        return IntentType.ACCESS_INVESTIGATION, subject_user, None

    if "risk" in q or "risky" in q:
        return IntentType.RISK_ANALYSIS, subject_user, None

    if "audit" in q or "list" in q:
        return IntentType.AUDIT, subject_user, None

    if "what if" in q or "remove" in q:
        return IntentType.POLICY_SIMULATION, subject_user, role

    raise ValueError("Unable to classify intent safely")
