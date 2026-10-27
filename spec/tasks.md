# Implementation Tasks and Acceptance Criteria

**Status**: Draft; tasks inherit the decision gates and phase ordering in [plan.md](./plan.md).  
**Requirements source**: [specification.md](./specification.md)  
**Governance**: [constitution.md](./constitution.md)  
**Clarification register**: [clarify.md](./clarify.md)

## How to Use This Task List

- Tasks are ordered by dependency, not by calendar date or assigned owner.
- A task is complete only when every acceptance criterion is met, evidence is reviewable, and applicable tests pass.
- Do not mark an approval-dependent implementation task complete using an assumed policy. Resolve its decision task first, or leave the dependent capability explicitly disabled.
- `Depends on` names task IDs in this file. `Gate` identifies a decision/approval needed before implementation; it is not permission to bypass an unresolved decision.
- Shared quality, safety, privacy, and documentation criteria apply to every implementation task; phase-specific criteria below add measurable completion checks.

## Phase 0 — Product Decisions and Delivery Baseline

### T0.1 — Approve product scope and release boundaries

**Depends on**: None  
**Gate**: Product owner and QA lead decisions  
**References**: C-06, T-01, T-03, T-04

**Acceptance criteria**
- [ ] Record whether this is a Vehicle Shop Jira feature within a broader Jira/Confluence product or a separately scoped product.
- [ ] Record which journeys may be authored, reviewed, approved, mapped, and executed in the pilot versus later phases.
- [ ] Record that Confluence access is disabled and out of scope for this release unless separate requirements and approval are accepted.
- [ ] Name pilot acceptance authority, evidence artifact, and sign-off requirements.
- [ ] Update specification and backlog wording so no pilot capability is ambiguous or contradictory.

### T0.2 — Approve environment and production safety policy

**Depends on**: T0.1  
**Gate**: Application/environment owner approval  
**References**: C-04, C-05, C-21

**Acceptance criteria**
- [ ] Record each pilot environment name and its owner-confirmed canonical base origin.
- [ ] Record who may add/change origins and the approval/distribution process for policy changes.
- [ ] Define production denial independently of the allowlist and document the trusted source for the denial policy.
- [ ] Define canonical URL parsing and comparison rules, including scheme, host, port, user-info, path, redirects, and malformed inputs.
- [ ] Define the browser boundary to enforce (top-level navigation only or additional requests/popups/service workers) and the required fail-closed behavior.
- [ ] Record the exact approved Sandbox origin and owner confirmation that it is non-production.

### T0.3 — Approve identity, roles, and authorization

**Depends on**: T0.1  
**Gate**: Organization identity/security owner approval  
**References**: C-02, C-16

**Acceptance criteria**
- [ ] Record the approved user authentication mechanism and how the API validates identity.
- [ ] Define role/action permissions for authoring, review, approval, run initiation, and administration.
- [ ] Record whether self-approval is allowed and define access revocation behavior.
- [ ] Define audit identity and required immutable or append-only events.
- [ ] Specify how secrets are supplied, rotated, and excluded from logs and committed files.

### T0.4 — Decide catalog authority and concurrency semantics

**Depends on**: T0.1  
**Gate**: Product and QA owner approval  
**References**: C-01, C-12, C-19

**Acceptance criteria**
- [ ] Declare PostgreSQL or a shared Excel workbook as the catalog source of truth.
- [ ] Define whether Excel files are snapshots, editable round-trips, imports, exports, or a combination.
- [ ] Define conflict detection, stale-write response, user resolution behavior, version history, and recovery.
- [ ] Define import atomicity: all-or-nothing or supported partial acceptance with explicit row-level results.
- [ ] Define supported template versions, sheets, workbook features, and maximum import size/row count.

### T0.5 — Define runner execution boundary and lifecycle

**Depends on**: T0.1, T0.3  
**Gate**: Product, security, and runner owners  
**References**: C-03, C-14

**Acceptance criteria**
- [ ] Select and record the runner deployment/execution model: user-operated CLI, local process, or separately deployed runner service.
- [ ] Define a versioned request/result contract carrying immutable selected case IDs, effective environment policy, and correlation/run ID.
- [ ] Define run states and transitions, including preflight refusal, confirmation, running, completed, failed, and cancelled as applicable.
- [ ] Define timeout, cancellation, retry, duplicate submission/idempotency, runner loss, and partial execution behavior.
- [ ] Define runner authentication and least-privilege access without placing secrets in command-line arguments or logs.

### T0.6 — Confirm Jira scope and query policy

**Depends on**: T0.1, T0.3  
**Gate**: Jira project owner and security approval  
**References**: C-07

**Acceptance criteria**
- [ ] Record the Jira Cloud base URL, project key, permitted issue types, fields, and read permissions.
- [ ] Approve issue-key lookup and the JQL capabilities, fields, functions, ordering, and result/pagination limits allowed to users.
- [ ] Define canonical browse-link generation/validation and handling of inaccessible or malformed issue data.
- [ ] Record the Jira credential source and explicit read-only enforcement expectations.
- [ ] If any input is unapproved, record Jira integration as disabled until approval rather than inventing a value.

### T0.7 — Record AI and Confluence decisions

**Depends on**: T0.1, T0.3, T0.6  
**Gate**: Organization provider/data governance and product approval  
**References**: C-08, C-09, T-04

**Acceptance criteria**
- [ ] Record whether AI drafting is approved; if approved, name the provider/deployment, permitted Jira fields, data-handling constraints, and approval owner.
- [ ] Define AI structured-output schema, request limits, timeout/retry/cost limits, and error behavior, or explicitly leave AI disabled.
- [ ] Define how issue content and generated text are treated as untrusted input.
- [ ] Record Confluence as disabled/out of scope for this release or add separately approved user needs, permitted scope, and read-only access requirements.
- [ ] Verify no credential or Jira content is sent to unapproved providers or Confluence endpoints.

### T0.8 — Approve data, artifacts, privacy, and service targets

**Depends on**: T0.1, T0.3  
**Gate**: Security, QA, and operations owner approval  
**References**: C-15–C-20, C-22

**Acceptance criteria**
- [ ] Define approved run artifact formats, destinations, access controls, retention/deletion, and screenshot/trace policy.
- [ ] Define data classification, encryption, redaction rules, audit events, backup/restore expectations, and secret rotation.
- [ ] Define whether PostgreSQL/Docker is development-only and document production database expectations separately.
- [ ] Define the intended 10-person concurrency profile and any measurable latency, availability, recovery, or usability targets.
- [ ] Define stable user-facing error categories, safe remediation guidance, and correlation-ID behavior.
- [ ] Record supported desktop Chrome and operating systems for the runner.

### T0.9 — Finalize contracts and pilot acceptance checklist

**Depends on**: T0.1–T0.8  
**Gate**: Product and QA sign-off  
**References**: C-10–C-22, SC-001–SC-010

**Acceptance criteria**
- [ ] Specify case fields, types, allowed values, limits, ID format/uniqueness, Jira relationship cardinality, step grammar, and approval invalidation rules.
- [ ] Specify review-state transitions, reviewer history, rejection reason policy, and deletion/archive rules.
- [ ] Specify catalog, run, case-result, error, and API contracts and their versioning approach.
- [ ] Define measurable pilot case count/outcome expectations, concurrency test scenarios, and evidence for each applicable success criterion.
- [ ] Update `specification.md`, `plan.md`, and this task list with decisions; unresolved features are explicitly blocked/disabled.

## Phase 1 — Platform Foundation

### T1.1 — Scaffold React 18/Vite client

**Depends on**: T0.1  
**References**: FR-025, FR-026

**Acceptance criteria**
- [ ] Client installs and starts using the approved project package scripts.
- [ ] Client builds with React 18 and Vite versions constrained by the repository's dependency policy.
- [ ] Client has no direct PostgreSQL connection or external-service credentials.
- [ ] A focused automated check verifies the production build succeeds.

### T1.2 — Scaffold Node.js/Express API and shared contracts

**Depends on**: T0.1, T0.9  
**References**: FR-025–FR-027, FR-030

**Acceptance criteria**
- [ ] API starts using documented commands and exposes a health/readiness response.
- [ ] Shared request/response contracts are versioned and validated at the API boundary.
- [ ] A representative invalid request returns the agreed stable error shape and status without internal secrets/stack traces.
- [ ] Automated checks cover API startup, health behavior, contract validation, and error serialization.

### T1.3 — Configure Docker PostgreSQL 15 and migrations

**Depends on**: T0.4, T0.8, T0.9  
**References**: FR-012, FR-025

**Acceptance criteria**
- [ ] Development Docker configuration pins PostgreSQL to major version 15.
- [ ] Committed environment examples contain placeholders only; no real database credentials are committed.
- [ ] A clean database can be initialized with repeatable, reviewable migrations.
- [ ] Migration/repository integration tests use a disposable PostgreSQL 15 database and synthetic data.
- [ ] Database unavailability and migration failure produce explicit, safely redacted errors.

### T1.4 — Establish test, quality, and local setup baseline

**Depends on**: T1.1–T1.3  
**References**: FR-028, FR-030; constitution Principle V

**Acceptance criteria**
- [ ] Document commands for installing dependencies, starting client/API/database, running focused tests, and resetting synthetic local data.
- [ ] Default tests do not require live Jira, Confluence, AI-provider, or Vehicle Shop credentials.
- [ ] External services and browser behavior are mocked/isolated in default tests.
- [ ] Test and quality commands are executable through documented project scripts.

## Phase 2 — Catalog, Case Authoring, and Human Review

### T2.1 — Implement test case and catalog persistence model

**Depends on**: T0.4, T0.9, T1.2, T1.3  
**References**: FR-007, FR-012; Key Entities

**Acceptance criteria**
- [ ] Database schema and migrations represent every approved Test Case field and catalog ownership/version data.
- [ ] Constraints enforce approved ID uniqueness and required relationships without silently dropping invalid values.
- [ ] Repository tests cover create, read, update, and validation failure using synthetic fixtures.
- [ ] The chosen source-of-truth and export/import semantics are reflected consistently in API and persistence contracts.

### T2.2 — Enforce user and role authorization

**Depends on**: T0.3, T1.2  
**References**: FR-001, FR-008, FR-009, FR-014, FR-027

**Acceptance criteria**
- [ ] API requests without valid identity are rejected using the approved auth behavior.
- [ ] Tests demonstrate each role can perform only its approved actions.
- [ ] Unauthorized review, approval, and run requests are rejected and create no state changes.
- [ ] Audit records use authenticated identity, not client-supplied reviewer/initiator names.

### T2.3 — Implement review state transitions and audit history

**Depends on**: T2.1, T2.2  
**References**: FR-008, FR-009

**Acceptance criteria**
- [ ] Only transitions in the approved transition graph are accepted.
- [ ] Each review decision records authenticated reviewer and timestamp, plus required reason/history fields.
- [ ] Generated/manual content remains Draft until an authorized explicit approval action.
- [ ] Changes to an Approved case follow the agreed invalidation/transition rule.
- [ ] Tests reject unauthorized, invalid, and stale transitions without partially changing the case.

### T2.4 — Implement catalog and field validation

**Depends on**: T0.9, T2.1  
**References**: FR-007, FR-010

**Acceptance criteria**
- [ ] Required field, type, length, enum, Jira reference, ID uniqueness, and numbered-step rules match the approved data contract.
- [ ] Validation errors identify the affected row/field or API field and provide an actionable reason.
- [ ] Tests cover missing/invalid values, duplicates, unsupported status/journey, invalid Jira links, and malformed steps.
- [ ] Invalid content is not persisted as a valid case.

### T2.5 — Implement safe Excel import

**Depends on**: T0.4, T0.9, T2.1, T2.4  
**References**: FR-011, SC-006

**Acceptance criteria**
- [ ] Supported `.xlsx` template versions and workbook features follow the approved policy.
- [ ] Import validates the complete file before committing data, or implements the explicitly approved partial-import contract.
- [ ] Invalid import does not corrupt or overwrite previously accepted catalog data.
- [ ] Row/column diagnostics identify all reported invalid entries.
- [ ] Tests cover malformed workbook, duplicates, unsupported features, size limits, and overwrite confirmation.

### T2.6 — Implement Excel export and round-trip behavior

**Depends on**: T0.4, T0.9, T2.1, T2.4  
**References**: FR-007, FR-011

**Acceptance criteria**
- [ ] Export contains all approved fields and canonical Jira traceability in the specified template.
- [ ] Export format, version, and snapshot/round-trip behavior are clearly identified.
- [ ] Valid export-import round-trip preserves all supported values and review metadata.
- [ ] Export failure is explicit and leaves source records unchanged.

### T2.7 — Implement concurrent edit/version conflict handling

**Depends on**: T0.4, T0.9, T2.1, T2.5  
**References**: SC-009

**Acceptance criteria**
- [ ] Stale updates are detected using the approved version/conflict mechanism.
- [ ] A concurrent edit cannot silently overwrite a newer accepted version.
- [ ] API and UI return the approved conflict code/message and recovery instruction.
- [ ] Deterministic two-writer tests verify expected conflict and recovery behavior.

### T2.8 — Implement React authoring and review workflows

**Depends on**: T2.1–T2.4, T2.7  
**References**: User Story 2; FR-007–FR-010

**Acceptance criteria**
- [ ] Authorized users can list, create, and edit cases through the Express API.
- [ ] Reviewers can perform permitted transitions and see reviewer/date/history.
- [ ] Loading, empty, validation, authorization, and conflict states are communicated accessibly.
- [ ] The UI never exposes external-service secrets or allows client-only authorization bypasses.

## Phase 3 — Read-Only Jira Integration and Controlled Drafting

### T3.1 — Implement Jira credential loading and read-only authentication

**Depends on**: T0.3, T0.6, T1.2  
**References**: FR-002, FR-003

**Acceptance criteria**
- [ ] Credentials load only from the approved environment/secret mechanism.
- [ ] Authentication failures are explicit and safely redacted.
- [ ] Tests assert credentials and authorization headers never appear in logs/errors.
- [ ] The adapter exposes no write operation to Jira.

### T3.2 — Implement constrained Jira issue-key retrieval

**Depends on**: T3.1  
**References**: FR-001, FR-002

**Acceptance criteria**
- [ ] Issue-key retrieval requests only approved fields and validates returned issue identity and canonical link.
- [ ] Missing, inaccessible, malformed, or out-of-scope issues return distinct actionable errors.
- [ ] Mocked tests cover valid issue, missing acceptance criteria, permissions, malformed response, and network error.

### T3.3 — Implement approved JQL search and pagination

**Depends on**: T0.6, T3.1  
**References**: FR-001, FR-002

**Acceptance criteria**
- [ ] User queries are limited to the approved project, issue types, fields, clauses, and result bounds.
- [ ] JQL is validated/encoded using the approved policy before transmission.
- [ ] Pagination, empty results, rate limits, and network errors are handled explicitly.
- [ ] Mocked tests prove disallowed scope cannot be queried and pagination has no duplicate/lost results.

### T3.4 — Build Jira story selection interface

**Depends on**: T3.2, T3.3, T2.8  
**References**: User Story 1; FR-001–FR-003

**Acceptance criteria**
- [ ] Authorized users can search by permitted issue key and approved JQL.
- [ ] Results show canonical issue key/link and only approved Jira fields.
- [ ] Empty, loading, rate-limit, permission, and service-error states are distinguishable.
- [ ] Tests verify the interface calls only the Express API and no Jira credentials are present client-side.

### T3.5 — Implement manual Draft authoring from Jira stories

**Depends on**: T2.8, T3.4  
**References**: FR-004, FR-007, FR-009

**Acceptance criteria**
- [ ] A selected Jira story can be used to create one or more manually authored cases.
- [ ] Every created case preserves the canonical source key/link and begins in Draft.
- [ ] Missing acceptance criteria are reported; no untraceable success-shaped cases are saved.
- [ ] Tests assert draft state and traceability on all manual creation paths.

### T3.6 — Implement AI provider adapter behind explicit approval gate

**Depends on**: T0.7, T3.4, T3.5  
**Gate**: Approved provider and data-sharing record  
**References**: FR-004–FR-006; constitution Principle II

**Acceptance criteria**
- [ ] Without approval/configuration, AI drafting is visibly disabled and transmits zero story content.
- [ ] When approved, only permitted minimum Jira fields are sent through the replaceable adapter.
- [ ] Requests enforce approved size/time/retry limits and surface provider failures.
- [ ] Responses are schema-validated; malformed/incomplete responses are rejected.
- [ ] Valid generated cases preserve source traceability and always start in Draft.
- [ ] Tests use a fake provider and cover disabled, timeout, invalid response, and success paths.

## Phase 4 — Safety-Gated Runner Integration and Reporting

### T4.1 — Define and version fixed automation registry

**Depends on**: T0.5, T0.9  
**References**: FR-016, FR-018

**Acceptance criteria**
- [ ] Registry schema defines automation ID, implementation binding, trusted journey classification, and policy metadata.
- [ ] Registry version can be recorded with a case/run as approved.
- [ ] Unknown, retired, or unimplemented IDs fail closed with actionable errors.
- [ ] Tests prove workbook-provided text is never evaluated or dynamically imported.

### T4.2 — Implement URL parsing, environment allowlist, and production denial

**Depends on**: T0.2, T0.5  
**References**: FR-017; SC-003

**Acceptance criteria**
- [ ] URL parsing follows the approved canonicalization rules.
- [ ] Scheme/host/port allowlist and independent production denial are enforced before every in-scope navigation.
- [ ] Malformed URLs, user-info, lookalike origins, unapproved ports, and unsafe redirects are denied before navigation.
- [ ] Missing, stale, or unavailable policy configuration fails closed.
- [ ] Deterministic tests cover normalization edge cases and verify zero navigation/network action on denied inputs.

### T4.3 — Implement case preflight and trusted booking policy

**Depends on**: T2.3, T2.4, T4.1, T4.2  
**References**: FR-015, FR-018; SC-002, SC-004

**Acceptance criteria**
- [ ] Preflight rejects unapproved states, malformed/duplicate selection, missing mappings, and unimplemented IDs before browser launch.
- [ ] Booking classification comes only from trusted registry/case metadata.
- [ ] Booking preflight enforces the approved Sandbox origin regardless of editable workbook content.
- [ ] Fake-browser matrix covers supported environments and representative title/step tampering, proving zero navigation when denied.

### T4.4 — Implement Node-to-Python runner adapter

**Depends on**: T0.5, T1.2, T4.1–T4.3  
**References**: FR-020, FR-026–FR-028

**Acceptance criteria**
- [ ] Express submits the approved versioned request with immutable case IDs, environment/policy, run ID, and correlation ID.
- [ ] Runner authenticates using the approved mechanism and receives no secrets in command-line arguments or logs.
- [ ] Responses/errors validate against the agreed contract and reject malformed or mismatched run IDs.
- [ ] Contract tests run using a fake runner and do not launch a live browser.

### T4.5 — Implement run confirmation and lifecycle

**Depends on**: T0.5, T0.9, T4.3, T4.4  
**References**: FR-013–FR-015, FR-024

**Acceptance criteria**
- [ ] UI displays exact cases and effective environment(s) before requesting explicit confirmation.
- [ ] Cancellation/no confirmation produces no browser launch or navigation.
- [ ] Approved run states and transitions are enforced, including refusal/cancellation/timeout/runner loss as specified.
- [ ] Duplicate requests follow the idempotency policy; retries/cancellation follow approved semantics.
- [ ] Tests verify all refusal and cancellation paths create no browser activity.

### T4.6 — Persist run and case result records

**Depends on**: T1.3, T0.9, T4.4, T4.5  
**References**: FR-021; Key Entities

**Acceptance criteria**
- [ ] Each run records unique ID, initiator, timestamps, selected cases, effective environment, browser, totals, and lifecycle state.
- [ ] Each case result records status, actionable details, and Jira traceability.
- [ ] Stored totals agree with per-case results, including the approved behavior for refused/skipped cases.
- [ ] Persistence tests cover partial execution, runner loss, duplicate result delivery, and failed database writes.

### T4.7 — Generate and securely store run artifacts

**Depends on**: T0.8, T4.6  
**References**: FR-022, FR-023

**Acceptance criteria**
- [ ] Outputs use the approved machine-readable and human-readable formats.
- [ ] Artifacts are stored only in approved locations with approved access and retention.
- [ ] Credentials, tokens, personal data, and payment data are redacted according to the policy.
- [ ] Artifact-store failure is explicit and does not report a successful artifact write.
- [ ] Tests cover format completeness, access policy, retention metadata, redaction, and write failures.

### T4.8 — Build React run selection, confirmation, and results views

**Depends on**: T4.3–T4.7  
**References**: User Stories 3–4

**Acceptance criteria**
- [ ] Authorized users can select eligible cases and an allowed environment.
- [ ] The confirmation view displays the exact selected cases and effective environment(s).
- [ ] Run progress, terminal states, per-case outcomes, totals, Jira links, and actionable failures are displayed from API data.
- [ ] UI loading, empty, denied, error, cancellation, and partial-result states are clear and accessible.

## Phase 5 — Search and Comparison Pilot

### T5.1 — Provision approved pilot prerequisites

**Depends on**: T0.2, T0.8, T0.9  
**Gate**: Environment/application owner approval  
**References**: FR-019, FR-020

**Acceptance criteria**
- [ ] Owner-approved pilot URLs and non-production classification are recorded.
- [ ] Dedicated test accounts and login instructions are provisioned through approved channels.
- [ ] Named synthetic data and repeatable setup/reset/cleanup procedures are documented.
- [ ] Missing prerequisites block pilot execution with explicit remediation details.

### T5.2 — Implement approved search and comparison automations

**Depends on**: T5.1, T4.1–T4.5  
**References**: User Story 5; FR-020

**Acceptance criteria**
- [ ] A small approved set of search and comparison cases uses desktop Chrome, stable approved selectors, and maintainable page objects.
- [ ] Each case has an approved review state, Jira traceability, and a fixed registry mapping.
- [ ] Setup and cleanup execute for success and failure scenarios.
- [ ] Automated tests use fixtures/mocks by default; live pilot checks target only explicitly approved non-production URLs.

### T5.3 — Execute end-to-end pilot acceptance

**Depends on**: T5.1, T5.2, T3.4–T3.5, T4.5–T4.8  
**Gate**: QA lead and designated product/environment sign-off  
**References**: SC-001–SC-010

**Acceptance criteria**
- [ ] Complete an approved end-to-end search/comparison workflow from story selection/manual drafting through review, confirmation, execution, and reporting.
- [ ] Evidence demonstrates traceability, accurate run totals, synthetic data, cleanup, secret redaction, and approved-origin-only activity.
- [ ] No production, unapproved origin, live payment, or booking action is contacted.
- [ ] All applicable pilot acceptance criteria pass; defects and known limitations are recorded.
- [ ] QA/environment owners record go/no-go decision for expansion.

## Phase 6 — Configuration and Sandbox Booking Expansion

### T6.1 — Approve configuration journey scope and test data

**Depends on**: T5.3  
**Gate**: Product/QA/environment owner approval  
**References**: User Story 6; C-06

**Acceptance criteria**
- [ ] Configuration journey cases, environments, synthetic fixtures, and cleanup rules are documented and approved.
- [ ] Scope identifies which configuration actions are safe and excluded.
- [ ] Execution remains disabled until environment and test-data prerequisites are satisfied.

### T6.2 — Implement configuration automation

**Depends on**: T6.1, T4.1–T4.5  
**References**: User Story 6; FR-020

**Acceptance criteria**
- [ ] Approved configuration cases use the fixed registry and trusted metadata.
- [ ] Safety policy is enforced before navigation and remains consistent with runner policy.
- [ ] Setup, cleanup, error, and failure-path tests pass using synthetic data.
- [ ] Jira traceability and result reporting are preserved.

### T6.3 — Approve Sandbox booking behavior

**Depends on**: T5.3  
**Gate**: Application owner, QA lead, and security approval  
**References**: C-04, C-05; constitution Principle III

**Acceptance criteria**
- [ ] Application owner confirms the canonical Sandbox origin is non-production.
- [ ] Permitted booking/payment simulation behavior is explicitly listed; prohibited actions are explicit.
- [ ] Dedicated test accounts and synthetic booking data/reset/cleanup are documented.
- [ ] Mixed booking/non-booking run behavior and user confirmation display are approved.
- [ ] A signed booking safety checklist and rollback/stop conditions are recorded.

### T6.4 — Implement and separately accept Sandbox booking automation

**Depends on**: T6.3, T4.1–T4.7  
**Gate**: Booking safety sign-off before feature enablement  
**References**: User Story 6; FR-018–FR-020; SC-004

**Acceptance criteria**
- [ ] Booking is dispatched only through a fixed registry entry with trusted booking classification.
- [ ] Every relevant navigation/redirect is checked against the exact approved Sandbox origin.
- [ ] Parameterized tests cover selected environment, edited titles/steps, malformed/missing configuration, redirect attempts, and denied navigation.
- [ ] Denied paths demonstrate zero navigation/network activity at the approved enforcement boundary.
- [ ] No real customer, payment, production booking, or unauthorized action is used.
- [ ] Booking stays disabled until focused safety tests and separate owner sign-off pass.

## Phase 7 — Team Adoption and Operational Readiness

### T7.1 — Validate team concurrency and service targets

**Depends on**: T2.7, T4.6, T5.3  
**Gate**: Agreed concurrency and SLO targets from T0.8/T0.9  
**References**: C-19, C-20; SC-009

**Acceptance criteria**
- [ ] Test scenarios exercise the agreed simultaneous users, edits, imports, and runs for the 10-person team.
- [ ] Conflicts follow the approved policy and do not silently overwrite accepted data.
- [ ] Measured response/recovery results meet the approved thresholds, or deviations are explicitly accepted/remediated.
- [ ] Backup/restore, retention, access revocation, and artifact retrieval are exercised and documented.

### T7.2 — Complete operational documentation and support handoff

**Depends on**: T5.3; T6.4 when booking is enabled  
**References**: FR-030; C-15, C-16, C-22

**Acceptance criteria**
- [ ] Documentation covers setup, configuration placeholders, credentials, permissions, catalog import/export, review, run operations, safety gates, troubleshooting, retention, and recovery.
- [ ] Error categories and correlation IDs connect user-visible failures to redacted diagnostics.
- [ ] Operational owners, escalation route, secret rotation, backup, restore, and data-retention responsibilities are named.
- [ ] Support runbook is reviewed by the designated QA/operations owners.

### T7.3 — Review adoption and decide future scope

**Depends on**: T7.1, T7.2  
**Gate**: Product/QA review  
**References**: Plan M7.2; T-01, T-04

**Acceptance criteria**
- [ ] QA feedback and pilot/adoption outcomes are recorded with actionable follow-ups.
- [ ] Security/safety findings, data retention, operational cost, and known limitations are reviewed.
- [ ] Any proposed Confluence, CI/scheduled execution, extra-browser, API-testing, or Jira-write capability has separate approved requirements and constitution review.
- [ ] No out-of-scope capability is enabled solely because of the broader product name.

## Cross-Cutting Acceptance Criteria

Apply these to every implementation task:

- [ ] Automated tests cover normal behavior, invalid input, authorization failures, operational failures, and safety boundaries relevant to the change.
- [ ] Default test execution uses mocks/fixtures and requires no live external credentials or production access.
- [ ] Logs, reports, workbooks, and browser artifacts do not contain credentials, tokens, real customer data, or payment data.
- [ ] React communicates through Express; only the backend owns external integration credentials and PostgreSQL access.
- [ ] External integration errors and safety denials are visible and do not degrade into silent skips or success-shaped responses.
- [ ] User-facing workflow, configuration, or operational changes update the relevant documentation.
- [ ] Changes comply with the constitution; any required exception is handled through a reviewed constitution amendment before implementation.
