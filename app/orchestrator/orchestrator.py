from app.orchestrator.intent_classifier import classify_intent_and_entity
from app.orchestrator.models import OrchestratorPlan
from app.common.enums import IntentType

def build_execution_plan(query: str) -> OrchestratorPlan:
    intent, subject_user, role = classify_intent_and_entity(query)

    if intent == IntentType.ACCESS_INVESTIGATION:
        return OrchestratorPlan(
            intent=intent,
            required_sources=["falcon", "rma", "risk_engine"],
            llm_allowed=True,
            subject_user=subject_user
        )

    if intent == IntentType.RISK_ANALYSIS:
        return OrchestratorPlan(
            intent=intent,
            required_sources=["risk_engine"],
            llm_allowed=True,
            subject_user=subject_user
        )

    if intent == IntentType.AUDIT:
        return OrchestratorPlan(
            intent=intent,
            required_sources=["rma", "risk_engine"],
            llm_allowed=True,
            subject_user=subject_user
        )

    if intent == IntentType.POLICY_SIMULATION:
        return OrchestratorPlan(
            intent=intent,
            required_sources=["rma", "policy_simulator"],
            llm_allowed=True,
            subject_user=subject_user,
            target_role=role
        )

    raise ValueError("Unsupported intent")
