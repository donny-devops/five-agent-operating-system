from __future__ import annotations

import asyncio
import functools
import json
import logging
import time
from collections.abc import Callable
from typing import Any, TypeVar

from .models import AgentOutput, TaskPacket, generate_request_id
from .router import create_task_packet

# ---------------------------------------------------------------------------
# Structured JSON logger
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": %(message)s}',
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("multi_agent_os.orchestrator")

F = TypeVar("F", bound=Callable[..., Any])


# ---------------------------------------------------------------------------
# Retry decorator (exponential back-off, sync)
# ---------------------------------------------------------------------------
def retry(max_attempts: int = 3, base_delay: float = 0.5) -> Callable[[F], F]:
    """Decorator that retries *fn* up to *max_attempts* times on any Exception."""

    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = base_delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    if attempt == max_attempts:
                        raise
                    log.warning(
                        '{"event": "retry", "fn": "%s", "attempt": %d, "error": "%s"}',
                        fn.__name__,
                        attempt,
                        exc,
                    )
                    time.sleep(delay)
                    delay *= 2

        return wrapper  # type: ignore[return-value]

    return decorator


# ---------------------------------------------------------------------------
# Agent runner helpers
# ---------------------------------------------------------------------------
def _timed_agent(
    fn: Callable[..., AgentOutput],
    *args: Any,
    agent_name: str,
    request_id: str,
) -> AgentOutput:
    """Call *fn*, record wall-clock duration, handle exceptions gracefully."""
    t0 = time.monotonic()
    try:
        result = fn(*args)
        result.duration_ms = round((time.monotonic() - t0) * 1000, 2)
        log.info(
            '{"event": "agent_complete", "request_id": "%s", "agent": "%s", "status": "%s", "duration_ms": %s}',
            request_id,
            agent_name,
            result.status,
            result.duration_ms,
        )
        return result
    except Exception as exc:  # noqa: BLE001
        duration_ms = round((time.monotonic() - t0) * 1000, 2)
        log.error(
            '{"event": "agent_error", "request_id": "%s", "agent": "%s", "error": "%s", "duration_ms": %s}',
            request_id,
            agent_name,
            exc,
            duration_ms,
        )
        return AgentOutput(
            request_id=request_id,
            agent_name=agent_name,
            status="failed",
            output={},
            errors=[str(exc)],
            duration_ms=duration_ms,
        )


# ---------------------------------------------------------------------------
# Individual agent functions
# ---------------------------------------------------------------------------
@retry()
def run_data_synthesis(task: TaskPacket) -> AgentOutput:
    output = {
        "summary": task.objective,
        "key_facts": [task.original_request],
        "entities": {
            "people": [],
            "companies": [],
            "tools": [],
            "dates": [],
            "systems": [],
        },
        "success_criteria": [
            "Output directly addresses the request.",
            "Unsupported claims are avoided.",
            "Missing information is flagged.",
        ],
        "constraints": task.missing_inputs,
        "contradictions": [],
        "assumptions": ["No external source material was provided."],
        "confidence": "medium",
        "recommended_next_agent": task.route[1] if len(task.route) > 1 else "compliance_quality_agent",
    }
    return AgentOutput(task.request_id, "data_synthesis_agent", "success", output, "medium")


@retry()
def run_decision_making(task: TaskPacket, context: dict[str, Any]) -> AgentOutput:
    output = {
        "decision": "Proceed with the lowest-risk useful deliverable based on available information.",
        "options": [
            {
                "name": "Ask for more information first",
                "impact": 3,
                "effort": 1,
                "risk": 1,
                "confidence": 4,
                "speed": 2,
                "score": 11,
            },
            {
                "name": "Create a best-effort first draft with placeholders",
                "impact": 5,
                "effort": 2,
                "risk": 2,
                "confidence": 3,
                "speed": 5,
                "score": 13,
            },
        ],
        "recommended_option": "Create a best-effort first draft with placeholders",
        "rationale": "Progress beats waiting when the missing details can be represented as placeholders.",
        "risks": ["Output may require personalization before final use."],
        "mitigations": ["Run the Compliance & Quality Agent before delivery."],
        "human_approval_required": task.human_review_required,
        "next_agent": "content_outreach_agent" if "content_outreach_agent" in task.route else "compliance_quality_agent",
    }
    return AgentOutput(task.request_id, "decision_making_agent", "success", output, "medium")


@retry()
def run_content_outreach(task: TaskPacket, context: dict[str, Any]) -> AgentOutput:
    output = {
        "content_type": "business_response",
        "audience": "business user or prospect",
        "subject_lines": ["Next steps", "Quick follow-up", "Recommended path forward"],
        "primary_draft": (
            "Hi {{recipient_name}},\n\n"
            "Thanks for reaching out. Based on the request, the best next step is to clarify the goal, "
            "confirm the required inputs, and move forward with a practical first version.\n\n"
            "Best,\n{{sender_name}}"
        ),
        "alternate_drafts": [],
        "claims_requiring_verification": [],
        "placeholders": ["recipient_name", "sender_name"],
        "next_agent": "compliance_quality_agent",
    }
    return AgentOutput(task.request_id, "content_outreach_agent", "success", output, "medium")


@retry()
def run_compliance_quality(task: TaskPacket, context: dict[str, Any]) -> AgentOutput:
    issues: list[dict[str, str]] = []
    approved = not task.human_review_required

    if task.human_review_required:
        issues.append({
            "severity": "high",
            "category": "human_review_required",
            "description": "The request contains high-risk terms or regulated content indicators.",
            "fix": "Route to a human reviewer before delivery.",
        })

    serialized_context = json.dumps(context)
    if "{{" in serialized_context and "}}" in serialized_context:
        issues.append({
            "severity": "medium",
            "category": "unresolved_placeholder",
            "description": "The output contains unresolved placeholders.",
            "fix": "Replace placeholders before external delivery.",
        })
        approved = False

    status = "approved" if approved else ("escalate" if task.human_review_required else "revise")
    output = {
        "status": status,
        "overall_score": 92 if approved else 78,
        "checks": {
            "objective_alignment": "pass",
            "accuracy": "pass",
            "unsupported_claims": "pass",
            "privacy": "pass",
            "security": "pass" if not task.human_review_required else "warning",
            "tone": "pass",
            "formatting": "pass",
            "missing_placeholders": "warning" if issues else "pass",
        },
        "issues": issues,
        "approved_for_delivery": approved,
        "human_review_required": task.human_review_required,
        "revision_instructions": [issue["fix"] for issue in issues],
    }
    return AgentOutput(task.request_id, "compliance_quality_agent", "success", output, "high")


# ---------------------------------------------------------------------------
# Async workflow runner
# ---------------------------------------------------------------------------
async def run_workflow_async(user_request: str) -> dict[str, Any]:
    """Run the five-agent pipeline asynchronously."""
    request_id = generate_request_id()
    task = create_task_packet(request_id, user_request, metadata={"source": "local_demo"})
    context: dict[str, Any] = {"task_packet": task.to_dict(), "agent_outputs": []}

    log.info(
        '{"event": "workflow_start", "request_id": "%s", "route": %s}',
        request_id,
        json.dumps(task.route),
    )

    _AGENT_DISPATCH: dict[str, Callable[..., AgentOutput]] = {
        "data_synthesis_agent": lambda: run_data_synthesis(task),
        "decision_making_agent": lambda: run_decision_making(task, context),
        "content_outreach_agent": lambda: run_content_outreach(task, context),
        "compliance_quality_agent": lambda: run_compliance_quality(task, context),
    }

    for agent_name in task.route:
        fn = _AGENT_DISPATCH.get(agent_name)
        if fn is None:
            result = AgentOutput(
                request_id=request_id,
                agent_name=agent_name,
                status="failed",
                output={},
                errors=[f"Unknown agent: {agent_name}"],
            )
        else:
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda _fn=fn, _name=agent_name: _timed_agent(
                    _fn, agent_name=_name, request_id=request_id
                ),
            )
        context["agent_outputs"].append(result.to_dict())

    log.info(
        '{"event": "workflow_complete", "request_id": "%s", "agents_run": %d}',
        request_id,
        len(context["agent_outputs"]),
    )
    return context


def run_workflow(user_request: str) -> dict[str, Any]:
    """Synchronous entry-point — wraps run_workflow_async."""
    return asyncio.run(run_workflow_async(user_request))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the Five-Agent Operating System.")
    parser.add_argument(
        "--request",
        default="Create a sales dashboard starter proposal for a small business that needs CRM pipeline visibility.",
        help="Business request to process through the agent workflow.",
    )
    args = parser.parse_args()
    print(json.dumps(run_workflow(args.request), indent=2))
