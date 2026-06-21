# Security Policy

## Supported Versions

Security updates are provided for the actively maintained `main` branch and the latest tagged release.

| Version | Supported |
| --- | --- |
| `main` | Yes |
| latest stable release | Yes |
| older releases | No |

## Reporting a Vulnerability

Please do not open public issues for security vulnerabilities.

Report privately through GitHub private vulnerability reporting if enabled, or contact the maintainer directly.

Please include:

- affected component, agent, schema, workflow, or configuration
- clear reproduction steps or proof of concept
- impact assessment
- logs or sample payloads with secrets removed
- suggested mitigation, if available

## Scope

In scope:

- prompt or agent contract risks that could leak sensitive data
- unsafe workflow automation
- dependency or CI/CD supply-chain risks
- schema validation bypasses
- logging of sensitive input or output
- unsafe persistence of agent outputs

Out of scope:

- social engineering
- denial-of-service without a practical exploit path
- issues caused only by downstream deployment changes outside the project defaults

## Security Expectations

- Do not commit secrets, tokens, private prompts, or customer data.
- Treat agent inputs and outputs as potentially sensitive.
- Keep human review in the loop for irreversible actions.
- Use least-privilege credentials for integrations.
- Prefer short-lived credentials and GitHub Actions OIDC for cloud deployments.
