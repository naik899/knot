"""Query parsing and execution planning models."""

from typing import Any, Optional

from pydantic import BaseModel, Field


class QueryIntent(BaseModel):
    primary_goal: str = Field(description="fto_analysis, landscape, validity, corporate_intel, patent_search, product_match")
    entities: dict[str, list[str]] = Field(default_factory=dict)
    constraints: dict[str, Any] = Field(default_factory=dict)
    raw_query: str = ""


class AgentStage(BaseModel):
    agent_id: str
    task_type: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    depends_on: list[str] = Field(default_factory=list)


class ExecutionPlan(BaseModel):
    stages: list[AgentStage] = Field(default_factory=list)
    timeout_ms: int = 300000
    intent: Optional[QueryIntent] = None
