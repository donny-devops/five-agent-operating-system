# Changelog

All notable changes to **five-agent-operating-system** will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- `SCHEMA_VERSION = "1.1.0"` constant in `models.py` — now stamped on every `TaskPacket`
- `generate_request_id()` helper in `models.py` — UUID4-based request IDs replacing the hardcoded `"REQ-001"`
- `AgentOutput.duration_ms` field — wall-clock execution time per agent hop
- `RouteResult` dataclass in `router.py` — wraps the ordered route list with `confidence_score` (0.0–1.0) and `is_hard_route` flag
- Routing metadata now embedded in `TaskPacket.metadata["routing"]` for observability
- `retry()` exponential back-off decorator in `orchestrator.py`
- `_timed_agent()` helper — times each agent call and emits structured JSON log lines
- `run_workflow_async()` — async entry-point using `asyncio`; `run_workflow()` wraps it synchronously
- Structured JSON logging via Python `logging` module (replaces bare `print`)
- `tests/test_router.py` — 20 unit tests covering `detect_work_types`, `detect_risk`, `build_route`, `create_task_packet`
- `tests/test_models.py` — 15 unit tests covering `TaskPacket`, `AgentOutput`, `generate_request_id`
- `tests/test_orchestrator.py` — 18 unit/integration tests covering all agent functions and full `run_workflow`
- `.github/workflows/ci.yml` — GitHub Actions CI: ruff lint + pytest on Python 3.11 and 3.12
- `pyproject.toml` — project metadata, ruff rule sets (`E W F I B UP C4 SIM`), pytest config, setuptools discovery
- `CONTRIBUTING.md` — sixth-agent guide, handoff contract format, schema extension rules, conventional commit style

### Changed
- `models.py`: replaced `from datetime import datetime, timezone` with `from datetime import datetime, UTC` (fixes Ruff UP017)
- `models.py`: `AgentOutput.created_at` default now uses `datetime.now(UTC)` instead of `datetime.now(timezone.utc)`
- `router.py`: `build_route()` now returns `RouteResult` instead of `list[str]`
- `router.py`: `create_task_packet()` injects routing confidence metadata into `TaskPacket.metadata`
- `orchestrator.py`: `run_workflow()` now generates a unique UUID-based `request_id` per invocation
- All agent functions decorated with `@retry()` for transient fault tolerance

### Fixed
- Ruff lint rule `UP017` (`datetime-timezone-utc`) — all `timezone.utc` references replaced with `datetime.UTC`

---

## [1.0.0] — 2025-05-09

### Added
- Initial five-agent architecture: Intake & Routing, Data Synthesis, Decision-Making, Content & Outreach, Compliance & Quality
- `TaskPacket` and `AgentOutput` dataclasses in `src/multi_agent_os/models.py`
- Keyword-based deterministic router in `src/multi_agent_os/router.py`
- Linear synchronous `run_workflow()` orchestrator in `src/multi_agent_os/orchestrator.py`
- Agent markdown specs in `agents/`
- JSON schemas in `schemas/`
- Handoff protocol and operating playbook in `docs/`
- Sample task packet in `examples/`
