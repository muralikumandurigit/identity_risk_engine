from fastapi import FastAPI
from app.orchestrator.orchestrator import build_execution_plan
from app.orchestrator.models import OrchestratorRequest
from app.iam.falcon_mock import get_auth_context
from app.iam.rma_mock import get_user_access
from app.risk.risk_engine import compute_identity_risk
from app.simulation.policy_simulator import simulate_role_removal
from app.common.enums import IntentType
from app.llm.explainer import explain_access_decision

# app = FastAPI(title="GenAI Identity Copilot")

# @app.post("/query")
# def query_copilot(req: OrchestratorRequest):
#    plan = build_execution_plan(req.query)
#
#    return {
#        "user": req.user,
#        "query": req.query,
#        "execution_plan": plan.dict()
#    }



def main():
    query = input("Ask the Identity Copilot: ")
    plan = build_execution_plan(query)

    print("\n--- EXECUTION PLAN ---")
    print(plan)

    if not plan.subject_user:
        print("\n❌ No user identified in query")
        return
    
    falcon_data = {}
    rma_data = {}


    # -------- ACCESS INVESTIGATION FLOW --------
    if plan.intent == IntentType.ACCESS_INVESTIGATION:
        falcon_data = get_auth_context(plan.subject_user)
        print("\n[Falcon]")
        print(falcon_data)

        rma_data = get_user_access(plan.subject_user)
        print("\n[RMA]")
        print(rma_data)

        risk = compute_identity_risk(falcon_data, rma_data)
        print("\n[RISK ASSESSMENT]")
        print(risk)

        explanation = explain_access_decision(
            user=plan.subject_user,
            risk=risk
        )
        print("\n[LLM EXPLANATION]")
        print(explanation)

    # -------- POLICY SIMULATION FLOW --------
    if plan.intent.value == "policy_simulation":
        if not plan.target_role:
            print("\n❌ No role identified for simulation")
            return

        rma_data = get_user_access(plan.subject_user)
        print("\n[RMA]")
        print(rma_data)

        simulation = simulate_role_removal(rma_data, plan.target_role)
        print(f"\n[POLICY SIMULATION – Remove {plan.target_role}]")
        print(simulation)

        explanation = explain_access_decision(
            user=plan.subject_user,
            simulation=simulation
        )

        print("\n[LLM EXPLANATION]")
        print(explanation)

if __name__ == "__main__":
    main()

