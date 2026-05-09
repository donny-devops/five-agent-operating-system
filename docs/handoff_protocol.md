# Handoff Protocol

## Purpose

The handoff protocol prevents agent chaos. Each agent receives a structured input, performs one job, and returns a structured output.

## Standard Envelope

```json
{
  "request_id": "REQ-001",
  "from_agent": "intake_routing_agent",
  "to_agent": "data_synthesis_agent",
  "handoff_reason": "Need context extraction before content drafting.",
  "payload": {},
  "constraints": [],
  "required_output": "synthesis_brief"
}
```

## Handoff Rules

1. Every handoff must include `request_id`.
2. Every handoff must include the reason for routing.
3. Agents must not silently skip missing critical inputs.
4. Agents must flag uncertainty instead of laundering it into confidence.
5. External-facing content must go through Compliance & Quality.
6. High-risk work must be escalated to human review.
7. The final delivery package must include status: `approved`, `revise`, or `escalate`.

## Revision Loop

```text
Compliance & Quality Agent
        |
        +--> approved --> delivery
        |
        +--> revise --> previous responsible agent
        |
        +--> escalate --> human review
```

## Minimum Audit Log

Track these fields:

- request_id
- timestamp
- user_request
- agent_name
- input_hash
- output_hash
- status
- model/provider used
- token/cost estimate if available
- escalation reason
- human approver if applicable
