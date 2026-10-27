# Implementation Plan: Jira-Traceable Vehicle Shop Test Case Automation

**Status**: Draft — gated by product, security, and operational decisions below  
**Source specification**: [specification.md](./specification.md)  
**Governing principles**: [constitution.md](./constitution.md)  
**Open review questions**: [clarify.md](./clarify.md)

## Plan Conventions

- Phases are ordered by dependency and safety risk; they are not calendar estimates. No delivery dates or staffing assumptions are made because team capacity is unspecified.
- A milestone is complete only when its deliverables are reviewed, its exit criteria are demonstrated, and related tests pass.
- Do not bypass an unresolved decision with an implementation assumption where the clarification review marks the topic as blocking.
- The default release remains on-demand, browser-UI-only, Jira read-only, and production-denied. Confluence and AI remain disabled until their separate approval gates are satisfied.
- PostgreSQL 15 is the persistent application store; Excel `.xlsx` remains a required catalog interchange/template format. Resolve the system of record and conflict policy before implementing catalog writes.

## Critical Decision Gates

Resolve these in Phase 0 before building the dependent capabilities:

1. **Catalog ownership and concurrency** — PostgreSQL versus shared workbook authority, import/export semantics, version/conflict handling. See C-01 and C-12.
2. **Identity and authorization** — approved authentication, roles, review/run permissions, self-approval policy, audit identity. See C-02.
3. **Runner boundary** — where Python/pytest/Playwright runs, how Express submits immutable requests, lifecycle/status/result protocol, cancellation and retry behavior. See C-03 and C-14.
4. **Environment safety policy** — pilot targets, owner-confirmed canonical origins, independent production-denial criteria, allowlist ownership, booking behavior in mixed runs. See C-04 and C-05.
5. **Release scope** — which case journeys may be authored, approved, mapped, and executed during pilot; acceptance authority and evidence. See C-06.
6. **External service boundaries** — Jira site/project/fields/JQL/permissions; AI approval and minimum-data contract; explicit Confluence exclusion or separately approved requirements. See C-07 through C-09.
7. **Data and operations** — artifact location/retention, privacy/redaction/audit policy, database deployment and backup expectations, team concurrency and service targets. See C-15 through C-20.

If any gate remains unresolved, continue only with independent scaffolding, contracts, and isolated tests that do not encode the unresolved policy. Keep the affected integration or workflow disabled.

**Current environment-gate status**: Staging is proposed as the initial pilot environment, but its canonical origin and owner approval are missing. Production-denial criteria are in progress but lack a documented trusted source; the policy-change authority, browser enforcement boundary, and non-production Sandbox confirmation are also pending. Do not enable browser execution or booking.

## Phase 0 — Product Decisions and Delivery Baseline

**Objective**: Convert open questions into approved decisions and establish acceptance evidence before feature implementation.

**Milestones**

### M0.1 — Scope and release boundaries approved

- Proposed decision: this Vehicle Shop Jira test-automation feature belongs to the broader Jira/Confluence automation project; Confluence access is disabled and out of scope for this release unless separately approved.
- Proposed initial-pilot boundary: only vehicle search and comparison may be authored, reviewed, approved, mapped, and executed; configuration and booking are deferred from all pilot lifecycle stages.
- Staging is the proposed pilot environment, but keep it unauthorized and the pilot environment unresolved until the application/environment owner approves its canonical origin.
- Proposed pilot acceptance authority: QA lead together with product and environment owners. Required evidence: test results, safety checklist, known limitations, and recorded go/no-go sign-off.
- Record these as proposed decisions pending product-owner and QA-lead sign-off; do not treat them as approvals or enable gated behavior before approval.

**Exit criteria**: Product owner and QA lead approve the recorded release boundaries; the evidence package and sign-off requirements are identified; the specification and backlog no longer imply conflicting pilot capabilities.

### M0.2 — Policy and operational decisions recorded

- Resolve the critical decision gates above, prioritizing catalog source of truth, identity/roles, runner interface, environment policy, and artifact handling.
- Define the case/review/run/result data contracts, allowed values, state transitions, and error categories.
- Approve the Jira query scope and any AI provider/data-sharing approval. If approvals are unavailable, explicitly retain those functions as disabled.
- Define test-only data and account ownership, operational retention, and supported desktop Chrome/OS baseline.

**Exit criteria**: Decisions are recorded in the specification; unresolved items are clearly marked as release blockers or disabled features, not left as implicit developer choices.

## Phase 1 — Platform Foundation

**Objective**: Establish the approved application structure and data/API boundaries without enabling external integrations or browser execution.

**Milestones**

### M1.1 — React and Express foundations

- Establish the React 18/Vite client and Node.js/Express API within the existing project skeleton.
- Establish shared, versioned request/response contracts and API-boundary validation.
- Add basic client/API health and configuration diagnostics without exposing secrets.
- Add automated checks for UI build, API startup, API contract validation, and error response shape.

### M1.2 — PostgreSQL 15 development persistence

- Add Docker development configuration pinned to PostgreSQL major version 15, with placeholder-only environment examples and no committed credentials.
- Add repeatable migrations and repository/data-access boundaries.
- Add a synthetic-only local test setup, reset process, and database availability diagnostics.
- Resolve C-21's test strategy with unit tests using isolated dependencies and disposable PostgreSQL integration tests for migrations/repositories.

**Exit criteria**:

- A developer can start the client, API, and PostgreSQL 15 development dependency using documented commands.
- The React client accesses application data only through the Express API.
- Migrations can initialize a clean test database and tests leave no production or personal data.
- Missing configuration and database availability failures are explicit and safely redacted.

## Phase 2 — Catalog, Case Authoring, and Human Review

**Objective**: Deliver useful case management and review controls before connecting story-generation or browser-run integrations.

**Milestones**

### M2.1 — Case and review domain

- Implement approved Test Case and Review Decision contracts and persistence, using only approved fields/enumerations.
- Implement manual Draft creation/editing and the approved Draft, Needs Update, Approved, and Rejected transition graph.
- Enforce authorization at the API boundary and record reviewer identity, decision time, and required history/reasons as decided in Phase 0.
- Ensure changes to approved content invalidate approval or follow the approved transition policy.

### M2.2 — Catalog validation and Excel interchange

- Implement `.xlsx` import/export using the approved template version and explicit import/overwrite behavior.
- Validate required headers and fields, case ID uniqueness, Jira key/link format, journey/status values, and numbered steps.
- Return row/column-specific errors; preserve the last valid catalog when validation or persistence fails.
- Implement the approved concurrency/version strategy and explicit stale-write conflict behavior.
- Reject or safely handle unsupported workbook features such as macros and external links according to the agreed policy.

**Exit criteria**:

- Users can create and review cases with traceability fields, and unauthorized or invalid state transitions fail explicitly.
- Generated content cannot become Approved without a separate authorized review action.
- Valid workbook round-trips preserve supported data; invalid imports do not partially overwrite accepted catalog state.
- Concurrent updates follow the approved conflict policy, with a deterministic test for the expected result.

## Phase 3 — Read-Only Jira Integration and Controlled Drafting

**Objective**: Enable requirement retrieval and, only if approved, AI-assisted drafting without remote writes.

**Milestones**

### M3.1 — Secure Jira read-only adapter

- Implement local/approved-secret-manager credential loading and Jira Cloud authentication without logging credentials or authorization headers.
- Retrieve only approved fields for configured project/issue types, by issue key or approved JQL.
- Safely constrain and encode JQL; implement pagination, bounded result handling, rate-limit behavior, and explicit permission/network/empty/missing-criteria errors.
- Preserve canonical issue keys and validated browse links in case records and exports.
- Add mocked tests for pagination, no results, missing criteria, unauthorized access, rate limiting, malformed responses, and network failures.
- Verify through tests that no create/update/comment/attachment operation is available in this release.

### M3.2 — Drafting workflow with AI disabled by default

- Deliver reviewable manual drafting independently of an AI provider.
- Provide a clear disabled/unconfigured state for AI drafting until organizational provider and data-sharing approval is recorded.
- If approved, add a replaceable provider adapter with bounded minimum input, timeout/error handling, strict structured-output validation, and traceability preservation.
- Save every generated case as Draft; reject incomplete or malformed responses and never auto-approve.
- Test both the disabled path (no content transmitted) and the approved path using a fake provider only.

**Exit criteria**:

- Jira story retrieval works against test doubles without live credentials in the default suite and performs no remote writes.
- JQL stays within approved project, issue type, field, and result bounds.
- AI is disabled unless approvals are recorded; if enabled, only allowed data is sent and validated results remain Draft.
- Provider, Jira, permission, and data-validation errors are visible without leaking secrets.

## Phase 4 — Safety-Gated Runner Integration and Reporting

**Objective**: Connect application run requests to the Python browser runner only after execution policy and run protocol are approved.

**Milestones**

### M4.1 — Trusted automation registry and preflight policy

- Define and version the fixed automation-ID registry and trusted journey/policy metadata.
- Validate case state, automation mapping, duplicate selection, implementation status, and environment before launch.
- Implement exact-origin allowlisting, canonical URL parsing, independent production denial, and redirect/navigation checks at the runner boundary.
- Enforce booking-only-on-approved-Sandbox from trusted metadata, never workbook title or steps.
- Fail closed if policy/configuration is absent, invalid, stale, or cannot be verified.
- Build deterministic fake-browser tests proving denied cases and destinations cause zero navigation; extend coverage to the approved browser boundary identified in C-21.

### M4.2 — Run protocol and lifecycle

- Implement the approved Node-to-runner request/response boundary, including authentication, immutable case/environment input, and correlation/run IDs.
- Implement the approved run states, preflight refusal representation, confirmation, cancellation, timeout, retry, duplicate-submission, and runner-loss handling.
- Require the application to display the exact case IDs and effective environment(s) and receive explicit confirmation before execution.
- Keep any uncertain mixed booking/non-booking behavior fail-closed until C-05 is resolved.

### M4.3 — Result reporting and artifact controls

- Record unique run ID, initiator, start/end timestamps, selected cases, effective environment, browser, totals, per-case outcomes, actionable failures, and Jira links.
- Generate the approved machine-readable and human-readable formats.
- Store results only at the approved destination with approved access, retention, and redaction controls.
- Test result totals, partial/infrastructure failure behavior, cleanup failures, artifact write failures, and secret/sensitive-data redaction.

**Exit criteria**:

- Every unsafe, unconfirmed, unapproved, or non-implemented run is refused before browser launch and produces no prohibited network/navigation activity.
- Booking always targets only the owner-approved Sandbox origin; mixed-run behavior matches the explicit approved policy.
- Run state and result records are complete and internally consistent; artifact errors are surfaced and do not masquerade as success.
- Default tests use fake browser/runner and service dependencies, not production or live credentials.

## Phase 5 — Search and Comparison Pilot

**Objective**: Validate the complete workflow with a small approved search/comparison set and dedicated synthetic data.

**Milestones**

### M5.1 — Pilot prerequisites and scenarios ready

- Obtain owner-confirmed target URLs, dedicated test accounts, login instructions, and synthetic test data/setup/reset/cleanup procedures.
- Confirm environment allowlist and independent production-denial policy using the Phase 0 approval record.
- Implement a small set of approved search and comparison UI scenarios using desktop Chrome, stable application-approved selectors, and maintainable page objects.
- Verify every pilot case has Jira traceability, explicit review approval, and a mapped implemented automation ID.

### M5.2 — End-to-end pilot acceptance

- Exercise story selection/manual or approved drafting, catalog review/import-export, run selection/confirmation, browser execution, cleanup, and result reporting.
- Validate no production, unapproved origin, live payment, or booking action is contacted.
- Run the approved safety acceptance checklist and capture QA sign-off and known limitations.

**Exit criteria**:

- A QA user completes the approved end-to-end search/comparison flow with reproducible synthetic data and a traceable result summary.
- All pilot acceptance and safety criteria in SC-001 through SC-010 applicable to the pilot pass.
- QA lead and designated product/environment owners approve expansion or document required remediation.

## Phase 6 — Configuration and Sandbox Booking Expansion

**Objective**: Add higher-risk journeys only after the pilot is accepted and booking prerequisites are explicitly approved.

**Milestones**

### M6.1 — Configuration journey

- Confirm scope, scenarios, test data, and supported environment policy for configuration cases.
- Add configuration automation IDs through the reviewed fixed registry and implement UI tests only after required gates are configured.
- Add setup/cleanup and failure-path tests; preserve the same pre-navigation environment policy.

### M6.2 — Sandbox booking safety acceptance

- Obtain explicit application-owner confirmation that the canonical Sandbox target is non-production and safe for the allowed booking behavior.
- Provision dedicated accounts and synthetic booking data; document exactly which booking/payment simulation steps are permitted.
- Implement booking automation only through trusted registry metadata and enforce exact Sandbox-origin checks before every relevant navigation.
- Test selected-environment combinations, edited workbook attempts, redirects, malformed/missing config, and no-navigation denial behavior.
- Perform a separate booking safety sign-off before enabling it for users.

**Exit criteria**:

- Configuration/booking are disabled until their own prerequisites and approvals are recorded.
- Booking scenarios use no real customer, payment, or production booking data and cannot navigate outside the approved Sandbox origin.
- Phase expansion has explicit QA/environment-owner approval and passing focused safety tests.

## Phase 7 — Team Adoption and Operational Readiness

**Objective**: Validate the workflow with the full QA team and prepare approved operational practices without expanding scope implicitly.

**Milestones**

### M7.1 — Team concurrency and operational exercise

- Exercise catalog edits and runs using the agreed concurrency profile for the 10-person team.
- Validate conflict recovery, audit history, access control, backups/retention, run artifact access, and troubleshooting guidance.
- Measure agreed response-time, reliability, and recovery targets if defined in Phase 0.

### M7.2 — Adoption review and scope decision

- Collect QA feedback on review flow, case quality, run confirmation, failure diagnostics, and reports.
- Review pilot outcomes, security/safety findings, data retention, and operational costs.
- Decide through explicit scope review whether to propose Confluence features, CI/scheduled execution, additional browsers, API testing, or Jira writes. None are enabled by this plan without an approved specification and constitution review.

**Exit criteria**:

- Team concurrency and operational acceptance criteria pass with documented evidence.
- Known gaps, ownership, retention, recovery, and support responsibilities are documented.
- Any expansion is represented as separately approved requirements rather than inferred from the product name.

## Cross-Cutting Workstreams

These apply in every phase:

- **Security and privacy**: least privilege, secret management, authorization, input validation, redaction, audit trail, synthetic data, and review of external data flows.
- **Safety**: exact-origin and production checks at the last responsible moment, trusted registry dispatch, Sandbox-only booking, and fail-closed behavior.
- **Quality**: focused unit/integration/contract tests, mocked external dependencies, disposable PostgreSQL 15 test database where appropriate, and no default live-service credentials.
- **Accessibility and usability**: agree UI accessibility and browser support acceptance in Phase 0; expose loading, empty, error, confirmation, and conflict states clearly.
- **Documentation**: keep setup, configuration placeholders, integration permissions, catalog format, review workflow, run instructions, safety policy, troubleshooting, and retention guidance current.
- **Observability**: use correlation IDs and actionable error categories; redact sensitive details and avoid success-shaped fallbacks.

## Milestone Dependency Overview

| Milestone | Depends on | Can proceed if decisions remain open? |
|---|---|---|
| M0.1 Scope and release boundaries | Product/QA owners | No; required before user-facing scope is frozen |
| M0.2 Policy and operational decisions | M0.1, environment/Jira/security owners | Independent scaffolding only; blocked capabilities stay disabled |
| M1.1 React and Express foundations | M0.1, approved stack | Yes, for skeleton and isolated health/contract work |
| M1.2 PostgreSQL persistence | M0.2 data ownership | Schema prototyping can proceed; production behavior blocked until ownership/retention decisions |
| M2.1 Case and review domain | M0.2 identity and state decisions; M1.2 | No for authorized review/persistence semantics |
| M2.2 Excel interchange | M0.2 catalog/concurrency decisions; M2.1 | Validation logic can be tested locally; authoritative writes blocked |
| M3.1 Jira integration | M0.2 Jira scope/credentials | No live integration until owner approvals; mocked adapter work may proceed |
| M3.2 AI drafting | M0.2 AI data approval; M2.1, M3.1 | Manual drafting proceeds; provider integration remains disabled |
| M4.1–M4.3 Runner and reporting | M0.2 runner/environment/artifact decisions; M1–M2 | Fake-runner contracts and policy tests can proceed; browser launch stays disabled |
| M5.1–M5.2 Pilot | M2–M4 and owner-approved pilot prerequisites | No |
| M6.1–M6.2 Expansion | M5 sign-off and journey-specific approvals | No |
| M7.1–M7.2 Adoption | M5 pilot; M6 where expansion is approved | Team exercises can be planned; adoption sign-off waits for acceptance evidence |

## Overall Definition of Done

- All applicable functional requirements and acceptance scenarios for the released phase are implemented and tested.
- Constitution principles are satisfied; no credentials or real sensitive data are committed or logged.
- No generated case is implicitly approved; all runs require explicit confirmation and trusted policy enforcement.
- Environment and booking safety tests pass, including zero navigation on denied paths.
- Jira remains read-only and Confluence/AI remain disabled unless their approval gates are satisfied.
- Database migrations, API contracts, user-facing errors, data retention behavior, and documentation are reviewed.
- Product/QA owners accept the phase using recorded evidence; unresolved issues are tracked and disabled rather than silently assumed.
