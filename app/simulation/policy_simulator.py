from typing import Dict
from app.iam.rma_mock import get_role_definition

def simulate_role_removal(
    user_access: Dict,
    role_to_remove: str
) -> Dict:
    current_roles = user_access.get("roles", [])
    current_entitlements = user_access.get("entitlements", [])

    if role_to_remove not in current_roles:
        return {
            "changed": False,
            "message": f"Role '{role_to_remove}' not assigned"
        }

    role_def = get_role_definition(role_to_remove)
    lost_entitlements = role_def.get("entitlements", [])

    remaining_roles = [r for r in current_roles if r != role_to_remove]
    remaining_entitlements = [
        e for e in current_entitlements if e not in lost_entitlements
    ]

    return {
        "changed": True,
        "removed_role": role_to_remove,
        "lost_entitlements": lost_entitlements,
        "remaining_roles": remaining_roles,
        "remaining_entitlements": remaining_entitlements
    }
