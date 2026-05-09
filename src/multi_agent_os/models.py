from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Literal

Priority = Literal["low", "normal", "high", "urgent"]
RiskLevel = Literal["low", "medium", "high", "critical"]
AgentStatus = Literal["success", "revise", "escalate", "failed"]


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
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
