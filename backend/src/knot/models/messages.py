"""Inter-agent communication models."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    request_id: str = ""
    source_agent: str = ""
    target_agent: str = ""
    task_type: str = ""
    payload: dict[str, Any] = Field(default_factory=dict)
    priority: str = Field(default="medium", description="high, medium, low")
    timeout_ms: int = 300000


class AgentResponse(BaseModel):
    request_id: str = ""
    agent: str = ""
    status: str = Field(default="success", description="success, partial, failure")
    result: dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = Field(ge=0, le=1, default=1.0)
    execution_time_ms: float = 0
    errors: list[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
