# Operating Playbook

## 1. Intake

The Intake & Routing Agent receives every new request first.

It must decide:

- What is the user trying to accomplish?
- What type of work is this?
- What is the risk level?
- What is missing?
- Which agent should handle the next step?

## 2. Synthesis

The Data Synthesis Agent turns raw context into a usable brief.

Use it when the input includes:

- emails
- CRM notes
- meeting notes
- support tickets
- documents
- reports
- screenshots
- messy requirements
- competing stakeholder comments

## 3. Decision

The Decision-Making Agent is used when the workflow needs a recommendation.

Examples:

- Which lead should be prioritized?
- Which campaign should launch first?
- Which customer issue needs escalation?
- Which technical approach is lower risk?
- Should we send, revise, pause, or escalate?

## 4. Content

The Content & Outreach Agent creates usable communication.

Examples:

- sales emails
- follow-up sequences
- LinkedIn messages
- proposal blurbs
- landing page sections
- customer support responses
- internal status updates

## 5. Compliance & Quality

The Compliance & Quality Agent is the final gate.

It checks:

- Does the output answer the actual request?
- Are any claims unsupported?
- Are there unresolved placeholders?
- Is any sensitive data exposed?
- Is the tone professional?
- Is the output ready to ship?

## Recommended Human Approval Points

Require human review for:

- legal claims
- financial advice
- medical advice
- HR decisions
- regulated security guidance
- public brand statements
- customer commitments
- pricing promises
- SLA promises
- contractual language

## Practical Deployment Pattern

Start simple:

1. Run deterministic router rules.
2. Add LLM calls per agent.
3. Save every input/output.
4. Add QA gate before delivery.
5. Add human review for escalation.
6. Add metrics after the workflow is stable.

Do not optimize orchestration before the process works. Fancy failure is still failure.
