# Five-Agent Operating System

A practical multi-agent operating model for intake, synthesis, decisions, outreach, and quality control.

Built for service businesses, consulting workflows, internal ops, sales enablement, digital marketing, IT/cloud operations, and AI automation pipelines.

## Agent Lineup

| Agent | Primary Job | Output |
|---|---|---|
| Intake & Routing Agent | Capture request, classify work, assign priority, route to the right agent path | `TaskPacket` |
| Data Synthesis Agent | Convert messy inputs into structured facts, insights, risks, and source notes | `SynthesisBrief` |
| Decision-Making Agent | Compare options, score tradeoffs, choose next action, document rationale | `DecisionRecord` |
| Content & Outreach Agent | Produce customer-facing or internal content based on approved context | `ContentPackage` |
| Compliance & Quality Agent | Validate accuracy, policy, privacy, security, completeness, and delivery readiness | `QualityGateReport` |

## Default Workflow

```text
User / System Request
        |
        v
Intake & Routing Agent
        |
        +--> Data Synthesis Agent
                  |
                  v
          Decision-Making Agent
                  |
                  v
          Content & Outreach Agent
                  |
                  v
          Compliance & Quality Agent
                  |
                  v
          Approved Output / Revision Loop
```

## Recommended Repo Structure

```text
five-agent-operating-system/
├── agents/
│   ├── intake-routing-agent.md
│   ├── data-synthesis-agent.md
│   ├── decision-making-agent.md
│   ├── content-outreach-agent.md
│   └── compliance-quality-agent.md
├── config/
│   └── agents.yaml
├── docs/
│   ├── handoff_protocol.md
│   └── operating_playbook.md
├── examples/
│   └── sample_task_packet.json
├── schemas/
│   ├── task_packet.schema.json
│   └── agent_output.schema.json
└── src/
    └── multi_agent_os/
        ├── __init__.py
        ├── models.py
        ├── router.py
        └── orchestrator.py
```

## Core Design Principle

Do not let every agent do everything. That is how agent systems become expensive group chats with badges.

Each agent has one lane, one decision boundary, and one clean handoff contract.

## Fast Start

```bash
cd five-agent-operating-system
python -m src.multi_agent_os.orchestrator
```

The included Python scaffold is dependency-light and uses deterministic routing rules. Connect your preferred LLM provider inside `orchestrator.py` where marked.

## Production Hardening Checklist

- [ ] Add authentication for incoming requests.
- [ ] Store task packets and decisions in a database.
- [ ] Add audit logging for every handoff.
- [ ] Add source citations for generated claims.
- [ ] Add human approval checkpoints for legal, financial, medical, HR, and customer-facing claims.
- [ ] Add PII redaction before synthesis.
- [ ] Add rate limiting and retry logic.
- [ ] Add observability: request ID, latency, model cost, failure reason, escalation reason.
- [ ] Add regression tests for routing behavior.
- [ ] Add a quality threshold before content is allowed to ship.

## Ideal Use Cases

- Lead intake and qualification
- Sales operations quick-answer lane
- CRM pipeline setup
- Outreach email drafting
- SEO audit synthesis
- Proposal generation
- Support-ticket triage
- Business research summaries
- Internal decision memos
- Compliance and QA checks
