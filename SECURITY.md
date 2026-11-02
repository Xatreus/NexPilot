# Security Policy

## Current scope
NexPilot plans engineering tasks and inspects public GitHub metadata and file paths. It does not run repository code, execute shell commands, deploy infrastructure, or modify GitHub.

## Safe use
- Keep model API keys and GitHub tokens in local environment variables; never commit them.
- Treat task text, repository descriptions, filenames, and future retrieved content as untrusted.
- Do not expose the API publicly without authentication, rate limiting, and deployment hardening.
- The repository report is not a security audit and does not scan source code or dependency advisories.
- Model-generated plans are suggestions, not authorization to perform actions.

## Reporting
Report vulnerabilities privately using GitHub's private vulnerability reporting feature if enabled. Otherwise, open a minimal issue requesting a private channel without publishing exploit details or sensitive data.
