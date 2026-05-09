from __future__ import annotations

import json
from typing import Any

from .models import AgentOutput, TaskPacket
from .router import create_task_packet


def run_data_synthesis(task: TaskPacket) -> AgentOutput:
    output = {
        "summary": task.objective,
        "key_facts": [task.original_request],
        "entities": {
            "people": [],
            "companies": [],
            "tools": [],
            "dates": [],
            "systems": []
        },
        "success_criteria": [
            "Output directly addresses the request.",
            "Unsupported claims are avoided.",
            "Missing information is flagged."
        ],
        "constraints": task.missing_inputs,
        "contradictions": [],
        "assumptions": ["No external source material was provided."],
        "confidence": "medium",
        "recommended_next_agent": task.route[1] if len(task.route) > 1 else "compliance_quality_agent"
    }
    return AgentOutput(task.request_id, "data_synthesis_agent", "success", output, "medium")


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
                "score": 11
            },
            {
                "name": "Create a best-effort first draft with placeholders",
                "impact": 5,
                "effort": 2,
                "risk": 2,
                "confidence": 3,
                "speed": 5,
                "score": 13
            }
        ],
        "recommended_option": "Create a best-effort first draft with placeholders",
        "rationale": "Progress beats waiting when the missing details can be represented as placeholders and reviewed before delivery.",
        "risks": ["Output may require personalization before final use."],
        "mitigations": ["Run the Compliance & Quality Agent before delivery."],
        "human_approval_required": task.human_review_required,
        "next_agent": "content_outreach_agent" if "content_outreach_agent" in task.route else "compliance_quality_agent"
    }
    return AgentOutput(task.request_id, "decision_making_agent", "success", output, "medium")


def run_content_outreach(task: TaskPacket, context: dict[str, Any]) -> AgentOutput:
    output = {
        "content_type": "business_response",
        "audience": "business user or prospect",
        "subject_lines": ["Next steps", "Quick follow-up", "Recommended path forward"],
        "primary_draft": (
            "Hi {{recipient_name}},\n\n"
            "Thanks for reaching out. Based on the request, the best next step is to clarify the goal, "
            "confirm the required inputs, and move forward with a practical first version that can be reviewed quickly.\n\n"
            "I can help structure the workflow, identify the key decisions, and produce a clean deliverable without overcomplicating the process.\n\n"
            "Would you be open to reviewing a first draft and confirming any missing details?\n\n"
            "Best,\n{{sender_name}}"
        ),
        "alternate_drafts": [],
        "claims_requiring_verification": [],
        "placeholders": ["recipient_name", "sender_name"],
        "next_agent": "compliance_quality_agent"
    }
    return AgentOutput(task.request_id, "content_outreach_agent", "success", output, "medium")


def run_compliance_quality(task: TaskPacket, context: dict[str, Any]) -> AgentOutput:
    issues = []
    approved = not task.human_review_required

    if task.human_review_required:
        issues.append({
            "severity": "high",
            "category": "human_review_required",
            "description": "The request contains high-risk terms or regulated content indicators.",
            "fix": "Route to a human reviewer before delivery."
        })

    # Simple placeholder check across collected outputs.
    serialized_context = json.dumps(context)
    if "{{" in serialized_context and "}}" in serialized_context:
        issues.append({
            "severity": "medium",
            "category": "unresolved_placeholder",
            "description": "The output contains unresolved placeholders.",
            "fix": "Replace placeholders before external delivery."
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
            "missing_placeholders": "warning" if issues else "pass"
        },
        "issues": issues,
        "approved_for_delivery": approved,
        "human_review_required": task.human_review_required,
        "revision_instructions": [issue["fix"] for issue in issues]
    }
    return AgentOutput(task.request_id, "compliance_quality_agent", "success", output, "high")


def run_workflow(user_request: str) -> dict[str, Any]:
    task = create_task_packet("REQ-001", user_request, metadata={"source": "local_demo"})
    context: dict[str, Any] = {"task_packet": task.to_dict(), "agent_outputs": []}

    for agent_name in task.route:
        if agent_name == "data_synthesis_agent":
            result = run_data_synthesis(task)
        elif agent_name == "decision_making_agent":
            result = run_decision_making(task, context)
        elif agent_name == "content_outreach_agent":
            result = run_content_outreach(task, context)
        elif agent_name == "compliance_quality_agent":
            result = run_compliance_quality(task, context)
        else:
            result = AgentOutput(task.request_id, agent_name, "failed", {}, errors=["Unknown agent"])
        context["agent_outputs"].append(result.to_dict())

    return context


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Run the Five-Agent Operating System."
    )

    parser.add_argument(
        "--request",
        default="Create a sales dashboard starter proposal for a small business that needs CRM pipeline visibility.",
        help="Business request to process through the agent workflow.",
    )

    args = parser.parse_args()

    print(json.dumps(run_workflow(args.request), indent=2))