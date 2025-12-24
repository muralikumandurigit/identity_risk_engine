from typing import Dict

# Simulated authentication/session data
_FAKE_SESSIONS = {
    "bob": {
        "user": "bob",
        "mfa": True,
        "device_trusted": False,
        "geo_location": "IN",
        "anomalous_login": True,
        "last_login": "2025-01-12T09:12:00Z"
    },
    "alice": {
        "user": "alice",
        "mfa": True,
        "device_trusted": True,
        "geo_location": "US",
        "anomalous_login": False,
        "last_login": "2025-01-12T08:55:00Z"
    }
}

def get_auth_context(user: str) -> Dict:
    """
    Simulates Falcon SSO session context.
    """
    return _FAKE_SESSIONS.get(user.lower(), {
        "user": user,
        "mfa": False,
        "device_trusted": False,
        "geo_location": "UNKNOWN",
        "anomalous_login": False,
        "last_login": None
    })
