"""Base agent abstract class with handle_request/execute lifecycle."""

import time
import uuid
from abc import ABC, abstractmethod

from knot.models.messages import AgentRequest, AgentResponse


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    agent_name: str = "base"

    @abstractmethod
    def execute(self, task_type: str, payload: dict) -> dict:
        """Execute the agent's core logic. Subclasses must implement this."""
        ...

    def handle_request(self, request: AgentRequest) -> AgentResponse:
        """Standard request handling lifecycle: validate, execute, respond."""
        start_time = time.time()
        request_id = request.request_id or str(uuid.uuid4())

        try:
            result = self.execute(request.task_type, request.payload)
            elapsed_ms = (time.time() - start_time) * 1000
            return AgentResponse(
                request_id=request_id,
                agent=self.agent_name,
                status="success",
                result=result,
                confidence_score=result.get("confidence_score", 1.0) if isinstance(result, dict) else 1.0,
                execution_time_ms=elapsed_ms,
            )
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            return AgentResponse(
                request_id=request_id,
                agent=self.agent_name,
                status="failure",
                result={},
                confidence_score=0.0,
                execution_time_ms=elapsed_ms,
                errors=[str(e)],
            )
