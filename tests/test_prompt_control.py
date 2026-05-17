from pathlib import Path

from src.multi_agent_os.prompt_control import (
    PROMPT_MANIFEST_DIR,
    apply_guardrails,
    evaluate_request,
    load_eval_fixtures,
    load_manifests,
    render_prompt_snapshot,
    score_telemetry,
    scrub_sensitive_fields,
    validate_agent_contract,
)


def test_load_manifests() -> None:
    manifests = load_manifests()
    assert len(manifests) >= 5
    assert "intake_routing_agent" in manifests


def test_prompt_snapshot_rendering() -> None:
    manifests = load_manifests()
    snapshot = render_prompt_snapshot(manifests["intake_routing_agent"])
    assert "agent_id: intake_routing_agent" in snapshot
    assert "Transform an unstructured request" in snapshot


def test_guardrail_detection() -> None:
    result = apply_guardrails("Use this api_key in production.")
    assert result.human_review_required is True
    assert result.allowed is True


def test_contract_validation() -> None:
    errors = validate_agent_contract(
        "content_outreach_agent",
        {
            "content_type": "email",
            "primary_draft": "Hello",
            "claims_requiring_verification": [],
            "next_agent": "compliance_quality_agent",
        },
    )
    assert "content_outreach_agent: missing audience" in errors
    assert "content_outreach_agent: missing subject_lines" in errors


def test_telemetry_scoring() -> None:
    guardrail = apply_guardrails("guarantee 100% results")
    telemetry = score_telemetry(
        "content_outreach_agent",
        {
            "content_type": "email",
            "audience": "prospect",
            "subject_lines": ["hello"],
            "primary_draft": "Hello",
            "alternate_drafts": [],
            "claims_requiring_verification": [],
            "placeholders": [],
            "next_agent": "compliance_quality_agent",
        },
        guardrail,
    )
    assert telemetry["quality_score"] < 100


def test_eval_harness() -> None:
    fixtures = load_eval_fixtures()
    assert len(fixtures) >= 4
    for fixture in fixtures:
        result = evaluate_request(fixture["request"])
        assert result["human_review_required"] == fixture["expect_human_review"]


def test_sensitive_field_scrubbing() -> None:
    payload = {"api_key": "example-value", "nested": {"password": "example-value"}}
    scrubbed = scrub_sensitive_fields(payload)
    assert scrubbed["api_key"] == "[REDACTED]"
    assert scrubbed["nested"]["password"] == "[REDACTED]"


def test_manifest_directory_exists() -> None:
    assert Path(PROMPT_MANIFEST_DIR).exists()
