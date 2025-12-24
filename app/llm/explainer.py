import json
from typing import Optional, Dict
import ollama

MODEL_NAME = "qwen2.5:7b"

SYSTEM_PROMPT = """
You are an enterprise Identity & Access Management (IAM) security assistant.

Rules:
- Explain ONLY the provided facts.
- Do NOT invent new risks, policies, or users.
- Do NOT recommend access approval or denial.
- Do NOT suggest enforcement actions.
- Be concise, neutral, and audit-friendly.
"""

def explain_access_decision(
    user: str,
    risk: Optional[Dict] = None,
    simulation: Optional[Dict] = None
) -> str:
    """
    Uses Qwen via Ollama to generate a human-readable explanation
    for IAM risk or policy simulation results.
    """

    context = {
        "user": user,
        "risk": risk,
        "simulation": simulation
    }

    prompt = f"""
{SYSTEM_PROMPT}

Context (JSON):
{json.dumps(context, indent=2)}

Task:
Explain the identity risk and/or policy impact in plain English.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"].strip()
