from typing import Dict, List

# Simulated authorization state
_USERS = {
    "bob": {
        "roles": ["prod_db_admin", "finance_viewer"],
        "entitlements": ["db:write", "db:read", "finance:read"]
    },
    "alice": {
        "roles": ["developer"],
        "entitlements": ["app:deploy", "app:read"]
    }
}

_ROLES = {
    "prod_db_admin": {
        "entitlements": ["db:write", "db:read"],
        "sod_conflicts": ["finance_viewer"]
    },
    "finance_viewer": {
        "entitlements": ["finance:read"],
        "sod_conflicts": ["prod_db_admin"]
    },
    "developer": {
        "entitlements": ["app:deploy", "app:read"],
        "sod_conflicts": []
    }
}

def get_user_access(user: str) -> Dict:
    """
    Returns user's roles and entitlements.
    """
    return _USERS.get(user.lower(), {"roles": [], "entitlements": []})

def get_role_definition(role: str) -> Dict:
    """
    Returns role definition including SoD conflicts.
    """
    return _ROLES.get(role, {"entitlements": [], "sod_conflicts": []})
