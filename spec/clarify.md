# Specification Review: Gaps, Contradictions, and Clarifications

**Reviewed documents**: [constitution.md](./constitution.md), [specification.md](./specification.md)  
**Review date**: 2026-10-27  
**Review status**: Draft review; the questions below should be resolved before implementation planning is treated as complete.

## Summary

The specification has a solid safety baseline and useful independently testable user journeys. The largest implementation blockers are unresolved ownership of catalog data, identity and authorization, environment/Jira configuration, run orchestration between the Node API and Python runner, and approved artifact storage. Several requirements state outcomes without defining the policy or measurable criteria needed to implement them consistently.

## Blocking Clarifications

### C-01. Catalog source of truth and synchronization

**References**: Summary; User Story 2; FR-007, FR-011, FR-012; Assumptions.

PostgreSQL is required for persistent application records, while Excel remains a required catalog format. The specification explicitly leaves unresolved whether Excel or PostgreSQL is authoritative, but also requires safe imports/exports, concurrent editing, conflict prevention, and preservation of existing data.

**Clarify**:
- Is PostgreSQL the authoritative catalog and Excel an import/export format, or is a shared workbook authoritative?
- If both may be edited, which wins on conflict and how are changes reconciled?
- What constitutes a concurrent edit conflict, and may users resolve it by reloading, merging, or creating a new version?
- Are workbook exports snapshots, editable round-trips, or both?

### C-02. User identity, authentication, and authorization

**References**: User Stories 1–3; FR-001, FR-008, FR-009, FR-014, FR-027; Assumptions.

The spec requires authorized users, authorized reviewers, attributable run initiators, and reviewer identity, but defines no sign-in mechanism, role model, provisioning process, or authorization behavior.

**Clarify**:
- How do users authenticate (for example, organization SSO, existing identity provider, or another approved mechanism)?
- Which roles exist, and which actions may each perform (author, reviewer, approver, run initiator, administrator)?
- Can users approve their own cases or initiate runs on cases they authored?
- How is identity authenticated at the API boundary and persisted in audit records?
- What happens when a user's access is revoked or they leave the team?

### C-03. Run orchestration and boundary between Node and Python

**References**: Summary; User Story 3; FR-013–FR-021, FR-026–FR-028; Technology and Operational Constraints.

The React/Express application is expected to coordinate runs, while browser automation remains in a separate Python/pytest/Playwright runner. The contract, deployment boundary, process lifecycle, and result-return path are unspecified.

**Clarify**:
- Does Express launch a local runner process, call a separately deployed runner service, or only create a run request for a user-operated CLI?
- Where does the runner execute, and how does it receive an immutable case selection and approved environment configuration?
- Is execution synchronous from the UI, asynchronous with polling, or event-driven?
- What are run timeout, cancellation, retry, duplicate-submission/idempotency, and runner-unavailable behaviors?
- How are runner authentication and least-privilege access handled without passing credentials in command-line arguments or logs?

### C-04. Approved environments, canonical origins, and hard production denial

**References**: User Story 3; User Story 5; User Story 6; FR-013, FR-017, FR-018; Technology and Operational Constraints; Assumptions.

The supported names are listed as Staging, Sandbox, QA, and PreProd, but the backlog says the pilot environments and canonical URLs still need owner confirmation. A hard production denial is required, yet its criteria in addition to the allowlist are unresolved.

**Clarify**:
- Which environments are in the first pilot, and what are their owner-confirmed canonical base URLs?
- Who may add/change an allowlisted origin, how is that change reviewed, and how does the runner receive updates?
- What precise host, DNS, network, or environment attributes establish that a URL is production and must be denied independently of the allowlist?
- How are URL normalization, default/explicit ports, case, trailing dots, IPv6, IDNs, user-info, paths, and DNS changes treated?
- Are only origins checked, or are allowed path prefixes also constrained?

**Partial response (pending application/environment-owner approval)**:
- Staging is proposed as the initial pilot environment. The response did not provide a valid canonical origin; the supplied value `2` is not recorded as an origin.
- The requester proposed themselves as the policy-change owner, but their authority and the approval/distribution process have not been verified.
- The independent production-denial policy is in progress; its trusted source and objective criteria remain unresolved.
- URL normalization and the browser enforcement boundary remain pending.
- No exact Sandbox origin or owner confirmation of its non-production status was provided. Booking remains disabled.
- No browser execution is authorized until the owner-approved origin and safety policy are recorded.

### C-05. Booking behavior in mixed-environment runs

**References**: User Story 3, acceptance scenario 5; User Story 6; FR-013, FR-018.

The user selects one general environment for a run, while booking cases must always use the approved Sandbox origin. The specification does not define whether a selection containing both booking and non-booking cases may split execution across environments or must be rejected.

**Clarify**:
- If a run includes both booking and non-booking cases and the user selects Staging, QA, or PreProd, should the system reject the entire run, split it so booking runs in Sandbox, or require separate runs?
- What environment is displayed and confirmed for each case when a run is split?
- Does any booking case force the entire run's selected environment to Sandbox?

### C-06. Pilot and feature release boundaries

**References**: User Story 5 and User Story 6; FR-004, FR-013, FR-024; Assumptions; constitution Principle V.

The pilot is described as search and comparison only, while case drafting covers all four journeys and environment selection includes all four environments. Configuration and booking are a later phase, but there is no feature flag or release gate defining what is visible, draftable, or executable in each phase.

**Clarify**:
- In the pilot, may users author/review configuration and booking drafts while execution remains disabled?
- Which environments are executable in the pilot?
- What exact evidence and sign-off constitute pilot acceptance, and who grants it?
- Are later-phase functions hidden, disabled with an explanation, or omitted until approved?

### C-07. Jira configuration, scope, and JQL policy

**References**: User Story 1; FR-001–FR-003; Technology and Operational Constraints; Assumptions.

The proposed project key `PROJECTCARS`, issue types, fields, Jira base URL, permissions, and JQL filter are not confirmed. "Approved user-supplied JQL" and "constrained to configured project and permitted issue types" do not describe how the application validates or restricts queries.

**Clarify**:
- What Jira Cloud site, project key, issue types, fields, and read permissions are approved?
- Is arbitrary user JQL supported, or only a constrained set of filters/clauses?
- Which JQL clauses, functions, fields, ordering, and result limits are allowed?
- How are encoded JQL, injection-like syntax, oversized results, pagination limits, and Jira API rate limits handled?
- Is the source canonical browse link built by the application or accepted from Jira's response, and how is its host validated?

### C-08. AI drafting approval and behavior

**References**: User Story 1; FR-004–FR-006; Assumptions; constitution Principle II.

AI drafting is a feature requirement, but the provider, approval process, permitted data, prompt/response contract, and operational limits are all unresolved. Manual authoring is allowed, but the required behavior while AI is disabled is not fully described.

**Clarify**:
- Which provider and deployment are approved, and who records/revokes approval?
- Exactly which Jira fields may be sent, under what retention/training/data-residency terms?
- What is the structured output schema, including journey, priority, steps, expected results, and traceability?
- What limits apply to request size, timeout, retries, cost, and provider availability?
- Should users be able to create/edit drafts manually before AI approval?
- How are Jira issue content and generated text treated as untrusted input to prevent instructions embedded in issue content from changing system behavior?

### C-09. Confluence scope

**References**: Project title/input; FR-003 and FR-029; Edge Cases; Assumptions; constitution Principle II.

The project is named Jira/Confluence automation, but the Vehicle Shop specification defines Jira story retrieval and no Confluence user journey. FR-029 says Confluence features remain disabled pending separate approval.

**Clarify**:
- Is Confluence explicitly out of scope for this feature/release, with no connection configured, or is read-only page retrieval expected?
- If retrieval is expected, what user need, spaces, page fields, permissions, search scope, and traceability are required?
- Is page authoring explicitly prohibited for this release?

## Major Behavioral and Data-Model Gaps

### C-10. Test-case fields, constraints, and enumerations

**References**: User Story 2; FR-007, FR-010; Key Entities.

The field list is present, but field types, required/optional status, limits, allowed values, and cross-field validation are not specified.

**Clarify**:
- Define valid journey values, priority values, automation status values, result values, and whether values are case-sensitive.
- Define case ID format, uniqueness scope, mutability, and behavior on duplicate IDs across catalogs.
- Define whether Jira keys may link to multiple cases and whether a case may trace to multiple Jira stories.
- Define field length limits, rich text/plain text rules, allowed URL formats, and numbered-step grammar.
- Define whether approval is invalidated when an approved case's content, source Jira story, or automation mapping changes.

### C-11. Review-state transition rules and audit history

**References**: User Story 2; FR-008, FR-009; Key Entities.

Four states are named, but the allowed transition graph and authorization rules are not.

**Clarify**:
- Which transitions are allowed (including transitions from Approved and Rejected)?
- Can an author edit an Approved case, and if so, does it return to Draft or Needs Update?
- Are reviewer, decision timestamp, and prior decisions stored as immutable history or overwritten with the latest values?
- Is a rejection reason or change request mandatory?
- Can cases be deleted, archived, or withdrawn after approval or after a run references them?

### C-12. Catalog import/export and concurrency semantics

**References**: User Story 2; FR-011; SC-006, SC-009.

Safe writes and concurrent-edit protection are required without defining file size, version identifiers, conflict detection, merge policy, supported Excel features, or export/import semantics.

**Clarify**:
- Which workbook template version/sheet names/headers are supported, and how are older templates migrated?
- What size/row limits apply, and are formulas, macros, external links, and hidden sheets rejected or preserved?
- How does the system detect a stale workbook or concurrent database update?
- On partial row errors, is the entire import rejected or are valid rows accepted with an explicit partial result?
- What is the precise overwrite confirmation and recovery/version-history behavior?

### C-13. Automation registry lifecycle and case mapping

**References**: User Story 3; FR-015, FR-016, FR-018, FR-020; Key Entities.

A fixed registry is required, but the schema, ownership, versioning, and relationship to persisted automation IDs are unspecified.

**Clarify**:
- Who adds or retires registry entries, and what review/tests are required?
- What happens to approved cases whose automation ID is removed, renamed, or no longer implemented?
- How is registry version recorded with the case and run?
- Which trusted metadata determines that an automation is a booking flow, and how is that classification tested?
- Can one automation ID map to multiple case types or environments?

### C-14. Run lifecycle, status model, and failures

**References**: User Story 3 and User Story 4; FR-014, FR-015, FR-021–FR-023; Key Entities.

The specification lists per-case pass/fail/skip totals but does not define run-level states or how cancellation, preflight refusal, infrastructure errors, partial execution, or cleanup failures affect them.

**Clarify**:
- Define run states (for example, pending, validating, awaiting confirmation, running, completed, failed, cancelled) and allowed transitions.
- Define whether a preflight refusal creates a recorded run and what status/results it has.
- Define how a runner crash or lost API connection is represented and reconciled.
- Define skip reasons, retry rules, timeout limits, and whether a retry creates a new run or another attempt within the same run.
- Define precedence when the assertion fails and cleanup also fails, and how both errors are reported.
- Define whether totals include cases refused before execution.

### C-15. Result artifact formats and storage

**References**: User Story 4; FR-021–FR-023; Key Entities; Assumptions.

Machine-readable and human-readable outputs are required, but their formats, locations, naming, permissions, retention, and download/access behavior are unresolved.

**Clarify**:
- Which machine format is required (for example JSON) and which human format is required (Markdown or HTML)?
- Are artifacts generated by the runner, API, or both, and where are they stored?
- Who may view/download a run, and can users access results after account removal?
- What are retention/deletion periods, backup expectations, and data-residency constraints?
- Are screenshots/traces enabled, and what redaction/approval checks apply before they are stored?

### C-16. Secret, privacy, and audit policy

**References**: Constitution Principles II and IV; FR-023, FR-027; Edge Cases; Non-Functional Requirements in the source specification.

The requirements prohibit sensitive data in logs and reports but do not define authentication secret storage, encryption, audit scope, or redaction guarantees.

**Clarify**:
- Which secret manager/configuration mechanism is approved for development and deployment?
- What encryption-in-transit and encryption-at-rest requirements apply to credentials, catalog records, and run artifacts?
- Which fields are considered personal, sensitive, or payment data, and how are they detected/redacted?
- What audit events must be immutable and retained (authentication, approvals, configuration changes, run actions, exports)?
- What are incident handling and secret rotation expectations?

### C-17. Database and Docker operational requirements

**References**: FR-012, FR-025; Technology and Operational Constraints; constitution Principle VI and Architecture and Data Boundaries.

PostgreSQL 15 via Docker and repeatable migrations are specified, but the operating model and data lifecycle are not.

**Clarify**:
- Is Docker/PostgreSQL for local development only, or is the production database also containerized?
- What database deployment, backup/restore, migration rollback, and upgrade policies apply?
- What is the expected persistence/retention policy for cases, reviews, runs, and results?
- Are local developer databases seeded only with synthetic data?
- What connection management, pooling, and service-unavailable behavior are required?

### C-18. API and frontend behavior

**References**: FR-025–FR-027; User Stories 1–4.

The stack is fixed but the contract and client behavior are not defined.

**Clarify**:
- Which API resource/operation boundaries are required for stories, cases, catalogs, approvals, runs, and results?
- What validation error shape, HTTP status conventions, pagination model, and API versioning policy apply?
- What loading, empty, retry, stale-data, and conflict states must the React interface expose?
- Are accessibility requirements (for example keyboard navigation, screen-reader labels, and contrast) part of acceptance?
- Which browsers/OSs are supported for the team UI? Desktop Chrome is specified for the automation runner, not clearly for the UI.

### C-19. Team concurrency and service-level expectations

**References**: User Stories 2 and 4; FR-011, FR-012; SC-009; source specification Non-Functional Requirements.

The application must support a 10-person QA team without overwrite, but has no quantitative performance, availability, or concurrency targets.

**Clarify**:
- Does "team of 10" mean 10 registered users, 10 simultaneous sessions, or 10 simultaneous edits/runs?
- What concurrent catalog edits, run count, and Jira requests must be supported?
- What response-time targets apply to typical catalog views, Jira searches, imports, and run-status updates?
- What uptime, recovery-time, and recovery-point objectives apply?
- Which operation-level locking/versioning strategy is expected, and how are users notified of conflicts?

## Contradictions and Scope Tensions

### T-01. Jira/Confluence project identity versus this feature's scope

**References**: User-provided project name; FR-003, FR-029; Assumptions; source project specification.

The requested product is described as Jira/Confluence automation, but this feature is specifically Vehicle Shop test-case automation sourced from Jira. Confluence is explicitly disabled and has no defined page workflow. Avoid treating the current feature as a complete Jira/Confluence product until Confluence requirements are added.

**Resolve by**: State whether this is one Jira-focused feature within a broader Jira/Confluence product, or rename/scope the feature to Vehicle Shop Jira test automation.

**Proposed resolution (pending product-owner and QA-lead sign-off)**: Treat this as a Vehicle Shop Jira test-automation feature within the broader Jira/Confluence project. Confluence access remains disabled and out of scope for this release.

### T-02. General environment selection versus booking's Sandbox-only rule

**References**: User Story 3; FR-013, FR-018.

The user selects one environment for the run, but booking must use Sandbox regardless of that selection. The mixed-run behavior is not defined, so two conforming implementations could execute different case sets or environments.

**Resolve by**: Answer C-05 and make the UI confirmation and runner contract express the selected environment per case or enforce a single-environment run.

### T-03. AI drafting for all journeys versus staged execution

**References**: User Story 1; User Story 5; User Story 6; FR-004, FR-005.

Drafting supports all four journeys, while search/comparison are the pilot and configuration/booking are later expansion. This may be intentional (draft early, enable execution later), but the feature flags and phase boundary are not explicit.

**Resolve by**: Specify which journeys may be authored, reviewed, approved, mapped, and executed during each phase.

**Proposed resolution (pending product-owner and QA-lead sign-off)**: During the initial pilot, only search and comparison cases may be authored, reviewed, approved, mapped, and executed. Configuration and booking are deferred from all pilot lifecycle stages and require a later scope decision; booking also requires its separate Sandbox safety approval.

### T-04. Confluence read-only default versus no Confluence requirement

**References**: FR-003, FR-029; Assumptions; constitution Principle II.

The constitution says Confluence is read-only by default, but FR-029 keeps page retrieval and authoring disabled until approval and requirements are defined. This is compatible only if "read-only by default" is a constraint on any future integration, not a feature enabled in this release.

**Resolve by**: Explicitly state that Confluence access is out of scope and disabled for this release; retain read-only as a future minimum-permission rule.

**Proposed resolution (pending product-owner and QA-lead sign-off)**: Confluence access is disabled and out of scope for this release. Any future approved access remains read-only by default and requires separately approved user needs, permitted content, and access scope.

### T-05. Test isolation versus required PostgreSQL persistence

**References**: FR-012, FR-028; User Story 2; constitution Principle V.

Persistent application records must use PostgreSQL, while the default test suite must mock or isolate database dependencies. It is unclear whether integration tests against an ephemeral PostgreSQL 15 instance are required or all database tests use mocks.

**Resolve by**: Define a test pyramid: unit tests with repository fakes/mocks, plus migration/repository integration tests against disposable PostgreSQL 15, with no production data.

## Measurability and Acceptance Gaps

### C-20. Success criteria need explicit thresholds and evidence

**References**: SC-001–SC-010.

Most criteria are testable as invariants, but several are not yet fully measurable or lack a named evidence source. SC-009 says conflicts are reported but has no concurrency scenario or required behavior; SC-010 has no owner/sign-off artifact; there are no latency or usability targets.

**Clarify**:
- Define concrete concurrency tests and expected conflict outcomes for SC-009.
- Identify the approver and checklist/evidence artifact for SC-010.
- Decide whether performance and usability targets are required for the pilot and, if so, set numeric thresholds and test conditions.
- Define how successful end-to-end pilot execution is measured, including number of cases and acceptable pass/fail/skip outcomes.

### C-21. Security and safety test coverage boundaries

**References**: User Stories 3 and 6; FR-015–FR-020, FR-028; SC-002–SC-004, SC-007.

The specification correctly requires no navigation on denied cases, but does not enumerate all safety-policy boundary cases or define the trusted source for environment configuration and redirects.

**Clarify**:
- Make the test matrix cover URL parsing/normalization, origin/port matching, production denial, redirect chains, browser popup/new-tab navigation, and navigation initiated after initial page load.
- Define whether every browser request or only top-level navigation is constrained; if requests are in scope, define behavior for subresources and service workers.
- Specify fail-closed behavior if configuration cannot be loaded or refreshed after preflight but before navigation.
- Define test evidence proving no network request occurred, rather than only asserting no navigation call in a fake browser.

### C-22. User-facing setup and error contracts

**References**: FR-030; Edge Cases; source specification Non-Functional Requirements.

Clear errors are required without defining error categories, actionable content, remediation guidance, or whether errors are exposed safely to users.

**Clarify**:
- Define stable error codes/categories for configuration, authentication, permissions, validation, safety denial, provider failure, database/storage failure, and runner failure.
- Specify which remediation hints are shown to users and which internal diagnostics are logged.
- Define correlation IDs so user-visible errors can be connected to redacted server/runner logs.

## Recommended Resolution Order

1. Resolve C-01 through C-06: source of truth, identity/authorization, runner architecture, approved environment policy, mixed booking runs, and phase boundaries.
2. Resolve C-07 through C-09: Jira query scope, AI approval/data contract, and explicit Confluence release scope.
3. Define the catalog/review/run/result data contracts in C-10 through C-15.
4. Define security, operations, API behavior, and team service levels in C-16 through C-19.
5. Convert C-20 through C-22 into measurable acceptance tests and operational error contracts.
