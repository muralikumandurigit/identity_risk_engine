from typing import List, Optional
from pydantic import BaseModel
from app.common.enums import IntentType

class OrchestratorRequest(BaseModel):
    user: str
    query: str

class OrchestratorPlan(BaseModel):
    intent: IntentType
    required_sources: List[str]
    llm_allowed: bool
    subject_user: Optional[str] = None
    target_role: Optional[str] = None
