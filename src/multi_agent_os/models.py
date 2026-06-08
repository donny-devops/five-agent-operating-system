from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal

Priority = Literal["low", "normal", "high", "urgent"]
RiskLevel = Literal["low", "medium", "high", "critical"]
AgentStatus = Literal["success", "revise", "escalate", "failed"]

SCHEMA_VERSION = "1.1.0"


@dataclass
class TaskPacket:
    request_id: str
    original_request: str
    objective: str
    work_type: list[str]
    priority: Priority = "normal"
    risk_level: RiskLevel = "low"
    missing_inputs: list[str] = field(default_factory=list)
    route: list[str] = field(default_factory=list)
    human_review_required: bool = False
    routing_reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentOutput:
    request_id: str
    agent_name: str
    status: AgentStatus
    output: dict[str, Any]
    confidence: Literal["low", "medium", "high"] = "medium"
    errors: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    duration_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def generate_request_id() -> str:
    """Generate a unique request ID using UUID4."""
    return f"REQ-{uuid.uuid4().hex[:12].upper()}"
