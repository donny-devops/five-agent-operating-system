---
name: add-new-agent-type
description: Workflow command scaffold for add-new-agent-type in five-agent-os.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /add-new-agent-type

Use this workflow when working on **add-new-agent-type** in `five-agent-os`.

## Goal

Adds support for a new agent type, including its prompt manifest and schema-validated contract.

## Common Files

- `prompts/agents/*.yaml`
- `schemas/contracts/*.contract.schema.json`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Create a new YAML prompt manifest in prompts/agents/
- Create a new JSON schema contract in schemas/contracts/

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.