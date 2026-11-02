# NexPilot Roadmap

## v0.1 — Engineering assistant foundation
- [x] Responsive dashboard and versioned API
- [x] Structured engineering plans with risks and acceptance criteria
- [x] Optional OpenRouter-compatible model with deterministic fallback
- [x] Public GitHub metadata/tree inspection
- [x] Local activity history and CLI plan command
- [x] Unit/API tests and CI foundation

## v0.2 — Repository-aware engineering
- [ ] Bounded retrieval of allowlisted text files
- [ ] Map entry points, modules, tests, manifests, and CI configuration
- [ ] Attach evidence paths to repository-specific findings
- [ ] Add fixture repositories and finding-precision evaluations
- [ ] Summarize CI runs using read-only permissions

## v0.3 — Knowledge and retrieval
- [ ] Index selected docs/source with source metadata
- [ ] Implement hybrid retrieval and evidence-grounded answers
- [ ] Evaluate chunking, relevance, citation correctness, and prompt-injection resistance
- [ ] Keep RAG optional and prevent indexing secrets by default

## v0.4 — Safe implementation loop
- [ ] Generate patch proposals on a working branch, never silently push to the default branch
- [ ] Show diffs and require approval before writes
- [ ] Run approved checks only in an isolated, resource-limited sandbox
- [ ] Record command output, test results, and audit events

## v0.5 — DevOps intelligence
- [ ] Summarize CI failures from provider APIs
- [ ] Analyze Docker and deployment configuration
- [ ] Add runbook retrieval and incident timelines
- [ ] Require least-privilege integrations and approval for deployment actions

## Release gates
Every milestone needs tests, documented configuration, bounded external calls, safe failures, no secret leakage, and clear capability limits. Roadmap items are not implemented until code and tests exist.
