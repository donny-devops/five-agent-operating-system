from __future__ import annotations

from .models import TaskPacket

HIGH_RISK_TERMS = {
    "legal", "lawsuit", "contract", "medical", "diagnosis", "therapy",
    "investment", "tax", "financial advice", "fire", "hire", "termination",
    "password", "api key", "secret", "payment", "credit card", "ssn", "pii"
}

WORK_TYPE_KEYWORDS = {
    "content_generation": ["email", "post", "copy", "proposal", "outreach", "linkedin", "landing page"],
    "decision_support": ["decide", "choose", "recommend", "prioritize", "score", "rank"],
    "research": ["research", "summarize", "analyze", "findings", "report"],
    "data_analysis": ["data", "spreadsheet", "csv", "dashboard", "metrics", "kpi"],
    "technical_implementation": ["build", "code", "api", "workflow", "integration", "repo", "deploy", "database"],
    "compliance_review": ["compliance", "policy", "quality", "qa", "review", "risk"]
}

ROUTES = {
    "content_generation": ["data_synthesis_agent", "content_outreach_agent", "compliance_quality_agent"],
    "decision_support": ["data_synthesis_agent", "decision_making_agent", "compliance_quality_agent"],
    "research": ["data_synthesis_agent", "decision_making_agent"],
    "data_analysis": ["data_synthesis_agent", "decision_making_agent", "compliance_quality_agent"],
    "technical_implementation": ["data_synthesis_agent", "decision_making_agent", "compliance_quality_agent"],
    "compliance_review": ["compliance_quality_agent"],
}


def detect_work_types(text: str) -> list[str]:
    lowered = text.lower()
    found: list[str] = []
    for work_type, keywords in WORK_TYPE_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            found.append(work_type)
    return found or ["unknown"]


def detect_risk(text: str) -> tuple[str, bool]:
    lowered = text.lower()
    if any(term in lowered for term in HIGH_RISK_TERMS):
        return "high", True
    return "medium", False


def build_route(work_types: list[str]) -> list[str]:
    """Build a stable phase-ordered route regardless of keyword order.

    This prevents awkward paths like QA before decision-making.
    """
    selected: set[str] = set()
    for work_type in work_types:
        selected.update(ROUTES.get(work_type, ["data_synthesis_agent", "decision_making_agent", "compliance_quality_agent"]))

    phase_order = [
        "data_synthesis_agent",
        "decision_making_agent",
        "content_outreach_agent",
        "compliance_quality_agent",
    ]
    return [agent for agent in phase_order if agent in selected]


def create_task_packet(request_id: str, user_request: str, metadata: dict | None = None) -> TaskPacket:
    work_types = detect_work_types(user_request)
    risk_level, human_review = detect_risk(user_request)
    route = build_route(work_types)

    objective = user_request.strip().rstrip(".")
    if not objective.lower().startswith(("create", "build", "draft", "analyze", "decide", "review", "summarize")):
        objective = f"Process request: {objective}"

    return TaskPacket(
        request_id=request_id,
        original_request=user_request,
        objective=objective,
        work_type=work_types,
        priority="normal",
        risk_level=risk_level,  # type: ignore[arg-type]
        missing_inputs=[],
        route=route,
        human_review_required=human_review,
        routing_reason="Route selected using keyword-based deterministic rules. Replace or enrich with model-based routing in production.",
        metadata=metadata or {},
    )
