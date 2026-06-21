```markdown
# five-agent-os Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill covers the core development patterns of the `five-agent-os` Python codebase. You'll learn the project's coding conventions, commit practices, and how to extend the system by adding new agent types using prompt manifests and schema contracts. This guide also explains the project's test structure and provides handy commands for common workflows.

## Coding Conventions

### File Naming
- **Style:** kebab-case
- **Example:**  
  ```
  agent-manager.py
  prompt-loader.py
  ```

### Import Style
- **Relative imports** are used within modules.
- **Example:**
  ```python
  from .utils import load_prompt
  ```

### Export Style
- **Named exports** are preferred.
- **Example:**
  ```python
  def create_agent(...):
      ...
  # Exported by name, not as default
  ```

### Commit Messages
- **Conventional commit format**
  - **Prefixes:** `feat`, `test`
  - **Example:**
    ```
    feat: add contract schema for planner agent
    test: add tests for agent loader
    ```

## Workflows

### Add New Agent Type
**Trigger:** When someone wants to introduce a new agent to the system.  
**Command:** `/new-agent-type`

1. **Create a prompt manifest:**  
   Add a new YAML file in `prompts/agents/` describing the agent's prompt.
   - **Example:**  
     `prompts/agents/my-new-agent.yaml`
2. **Create a contract schema:**  
   Add a new JSON schema file in `schemas/contracts/` to define and validate the agent's contract.
   - **Example:**  
     `schemas/contracts/my-new-agent.contract.schema.json`
3. **(Optional) Commit your changes:**  
   Use a conventional commit message, e.g.:
   ```
   feat: add prompt and contract for my-new-agent
   ```
4. **(Optional) Add tests:**  
   Create test files following the `*.test.*` pattern to verify your agent type.

## Testing Patterns

- **Test File Pattern:**  
  Test files are named with the pattern `*.test.*` (e.g., `agent-manager.test.py`).
- **Framework:**  
  No specific testing framework detected; use standard Python testing practices.
- **Example:**
  ```python
  # agent-manager.test.py
  def test_agent_creation():
      agent = create_agent(...)
      assert agent is not None
  ```

## Commands

| Command         | Purpose                                                        |
|-----------------|----------------------------------------------------------------|
| /new-agent-type | Scaffold and document the process to add a new agent type      |
```
