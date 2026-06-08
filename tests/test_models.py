"""Tests for src/multi_agent_os/models.py."""

from __future__ import annotations

from src.multi_agent_os.models import (
    SCHEMA_VERSION,
    AgentOutput,
    TaskPacket,
    generate_request_id,
)


# ---------------------------------------------------------------------------
# TaskPacket
# ---------------------------------------------------------------------------
class TestTaskPacket:
    def _make(self, **kwargs) -> TaskPacket:  # type: ignore[no-untyped-def]
        defaults = {
            "request_id": "REQ-TEST",
            "original_request": "Test request",
            "objective": "Test objective",
            "work_type": ["research"],
        }
        return TaskPacket(**{**defaults, **kwargs})

    def test_defaults(self) -> None:
        tp = self._make()
        assert tp.priority == "normal"
        assert tp.risk_level == "low"
        assert tp.missing_inputs == []
        assert tp.route == []
        assert tp.human_review_required is False
        assert tp.metadata == {}

    def test_version_equals_schema_version(self) -> None:
        tp = self._make()
        assert tp.version == SCHEMA_VERSION

    def test_to_dict_is_serializable(self) -> None:
        import json

        tp = self._make()
        d = tp.to_dict()
        # Must be JSON-serializable without errors
        json.dumps(d)

    def test_to_dict_contains_version(self) -> None:
        tp = self._make()
        assert "version" in tp.to_dict()

    def test_route_field_accepts_list(self) -> None:
        tp = self._make(route=["data_synthesis_agent", "compliance_quality_agent"])
        assert len(tp.route) == 2

    def test_metadata_field_accepts_dict(self) -> None:
        tp = self._make(metadata={"source": "test"})
        assert tp.metadata["source"] == "test"


# ---------------------------------------------------------------------------
# AgentOutput
# ---------------------------------------------------------------------------
class TestAgentOutput:
    def _make(self, **kwargs) -> AgentOutput:  # type: ignore[no-untyped-def]
        defaults = {
            "request_id": "REQ-TEST",
            "agent_name": "data_synthesis_agent",
            "status": "success",
            "output": {"summary": "ok"},
        }
        return AgentOutput(**{**defaults, **kwargs})

    def test_defaults(self) -> None:
        ao = self._make()
        assert ao.confidence == "medium"
        assert ao.errors == []
        assert ao.duration_ms == 0.0

    def test_created_at_is_iso_string(self) -> None:
        ao = self._make()
        # Should be parseable as an ISO datetime
        from datetime import datetime

        datetime.fromisoformat(ao.created_at)

    def test_to_dict_contains_duration_ms(self) -> None:
        ao = self._make(duration_ms=42.5)
        assert ao.to_dict()["duration_ms"] == 42.5

    def test_to_dict_is_serializable(self) -> None:
        import json

        ao = self._make()
        json.dumps(ao.to_dict())

    def test_errors_field(self) -> None:
        ao = self._make(status="failed", errors=["something broke"])
        assert ao.errors == ["something broke"]

    def test_status_values(self) -> None:
        for status in ("success", "revise", "escalate", "failed"):
            ao = self._make(status=status)  # type: ignore[arg-type]
            assert ao.status == status


# ---------------------------------------------------------------------------
# generate_request_id
# ---------------------------------------------------------------------------
class TestGenerateRequestId:
    def test_starts_with_req(self) -> None:
        rid = generate_request_id()
        assert rid.startswith("REQ-")

    def test_unique_ids(self) -> None:
        ids = {generate_request_id() for _ in range(100)}
        assert len(ids) == 100

    def test_length_reasonable(self) -> None:
        rid = generate_request_id()
        assert 10 <= len(rid) <= 30
