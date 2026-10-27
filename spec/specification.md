# Feature Specification: Jira-Traceable Vehicle Shop Test Case Automation

**Feature Branch**: `001-jira-test-case-automation`

**Created**: 2026-10-27

**Status**: Draft

**Input**: User description: "Based on the Vehicle Shop test case automation specification, define the application requirements using Spec Kit format. The approved application stack is React 18 with Vite, Node.js with Express, and PostgreSQL 15 via Docker."

## Summary

Provide a reviewable workflow for selecting Jira stories, maintaining traceable test cases, approving cases, running approved browser UI tests on demand, and reporting results. The intended users are a QA lead and a 10-person QA team. This feature covers the Vehicle Shop journeys: vehicle search, comparison, configuration, and booking.

The application will provide a team interface and backend while preserving the separately governed Python/pytest/Playwright browser runner. The Excel workbook remains a required catalog format. The relationship between the workbook and persistent application records requires confirmation (see Assumptions).

## User Scenarios & Testing

### User Story 1 - Select Jira stories and create traceable drafts (Priority: P1)

As a QA author, I want to select eligible Jira stories by issue key or an approved JQL filter and create candidate test cases, so that each candidate is linked to its source requirements.

**Why this priority**: Jira stories and acceptance criteria are the source material for the team's test cases. Traceability must exist from the start of the workflow.

**Independent Test**: Using mocked Jira responses, select a story with acceptance criteria and verify the resulting candidate cases preserve the canonical issue key/link and are all in Draft status. Run without Jira credentials in the default automated suite.

**Acceptance Scenarios**:

1. **Given** a configured, read-only Jira connection and an authorized issue key, **When** the user requests the story, **Then** the system returns the approved story fields and canonical issue key and browse link.
2. **Given** an approved, user-supplied JQL filter within the configured project and issue-type scope, **When** the user searches, **Then** the system returns matching stories with pagination handled and no write operations performed.
3. **Given** an eligible story with acceptance criteria and an approved, enabled AI provider, **When** the user requests case drafting, **Then** the system validates the structured result, preserves source traceability, and saves each new case as Draft.
4. **Given** there is no approved AI provider or data-sharing approval, **When** the user opens or requests AI drafting, **Then** drafting is disabled with a clear explanation and no story content is sent to a provider.
5. **Given** a story has missing acceptance criteria, **When** it is selected for drafting, **Then** the system reports that condition and does not create success-shaped or untraceable cases.

### User Story 2 - Maintain and review the test catalog (Priority: P1)

As a QA reviewer, I want to inspect and edit test cases in an Excel-compatible catalog, record review decisions, and retain reviewer attribution, so that only explicitly approved cases can proceed to execution.

**Why this priority**: Human review is the safety and quality gate between authored content and browser execution.

**Independent Test**: Import or create cases in a test fixture, validate required catalog fields, exercise each review transition, and verify reviewer/date attribution and rejection of invalid or duplicate rows.

**Acceptance Scenarios**:

1. **Given** a valid catalog row, **When** it is displayed or exported, **Then** it includes the required case fields and source Jira key/link.
2. **Given** a Draft case, **When** an authorized reviewer approves, rejects, or requests an update, **Then** the new state and reviewer/date are recorded.
3. **Given** a case has not been explicitly approved by an authorized reviewer, **When** generated or edited content is saved, **Then** the case does not become Approved automatically.
4. **Given** an uploaded workbook has missing headers, invalid values, duplicate case IDs, invalid Jira references, or malformed numbered steps, **When** it is validated, **Then** actionable errors identify the row and column and invalid data is not silently accepted.
5. **Given** a populated catalog is being updated, **When** a write fails validation or conflicts with a concurrent edit, **Then** the existing catalog is preserved and the failure is surfaced.

### User Story 3 - Run approved cases safely on demand (Priority: P1)

As a run initiator, I want to select approved, implemented cases and an allowed environment, review the exact selection, and explicitly confirm the run, so that browser automation runs only when intended and only in a safe environment.

**Why this priority**: Browser navigation can affect real environments. Approval, environment enforcement, and confirmation must be enforced before any browser action.

**Independent Test**: Use a fake browser and isolated runner/configuration fixtures. Verify the allowed path navigates only to the approved Sandbox origin and every invalid case, unsafe destination, or unconfirmed run is refused with zero navigation attempts.

**Acceptance Scenarios**:

1. **Given** the user selects cases and an allowed environment, **When** the run confirmation is presented, **Then** it shows the selected environment and exact case IDs before execution can begin.
2. **Given** the user cancels or does not confirm, **When** the run is submitted, **Then** no browser is launched and no navigation occurs.
3. **Given** a selection contains a Draft, Needs Update, Rejected, malformed, duplicate, unmapped, or non-implemented case, **When** preflight validation runs, **Then** the run is refused with actionable case-level errors before browser launch.
4. **Given** a configured URL is malformed, not explicitly allowlisted, points to production, or differs by scheme, hostname, or permitted port, **When** a run or redirect is checked, **Then** it is rejected before navigation.
5. **Given** a booking case is selected while another environment is selected or editable workbook text has been changed, **When** the runner resolves its trusted automation metadata, **Then** it permits navigation only to the approved Sandbox origin or refuses the run before navigation.
6. **Given** a browser starts, navigation fails, an assertion fails, or teardown fails, **When** the case finishes, **Then** required cleanup is attempted and the failure is recorded without exposing secrets or sensitive data.

### User Story 4 - Review run results and traceability (Priority: P1)

As a QA lead, I want a concise run summary and machine-readable result for each execution, so that the team can understand outcomes, investigate failures, and trace results to Jira.

**Why this priority**: A run without attributable, actionable results is not useful for QA sign-off or repeatability.

**Independent Test**: Feed deterministic passed, failed, and skipped case results to the reporting component and verify complete metadata, correct totals, per-case details, Jira links, and redaction.

**Acceptance Scenarios**:

1. **Given** a run has completed, **When** the result is recorded, **Then** it contains a unique run ID, start/end timestamps, selected environment, browser, selected case IDs, pass/fail/skip totals, per-case outcomes, and source Jira links.
2. **Given** a case fails, **When** the summary is viewed or exported, **Then** it includes actionable failure details and does not include credentials, tokens, personal data, or payment data.
3. **Given** the run has results, **When** the user requests output, **Then** the system produces a machine-readable result and a concise human-readable summary only in an approved location.
4. **Given** Jira is available or unavailable, **When** a run fails, **Then** the system reports the outcome and does not create or update Jira issues, comments, or attachments.

### User Story 5 - Pilot approved search and comparison journeys (Priority: P2)

As a QA team member, I want to run a small set of approved vehicle search and comparison cases using dedicated synthetic data, so that the team can validate the workflow before expanding coverage.

**Why this priority**: Search and comparison are the recommended initial pilot scope; they provide value without enabling booking prematurely.

**Independent Test**: Against a non-production fixture or explicitly approved Sandbox, run a small approved search/comparison set with repeatable setup and cleanup, then inspect the run summary and Jira traceability.

**Acceptance Scenarios**:

1. **Given** URLs, accounts, test data, and safety gates are approved, **When** an approved search or comparison case is run in the pilot environment, **Then** the case uses stable, application-approved UI selectors and records its result.
2. **Given** a test fails after creating or modifying synthetic state, **When** the case exits, **Then** cleanup/reset is attempted even when startup, navigation, assertion, or teardown fails.
3. **Given** pilot prerequisites or environment approvals are missing, **When** a user attempts to run a pilot scenario, **Then** the run is blocked with the missing prerequisite identified.

### User Story 6 - Expand to configuration and Sandbox booking (Priority: P3)

As an authorized QA lead, I want configuration and booking journeys added only after the pilot is accepted and booking safety is confirmed, so that higher-risk coverage does not precede its safeguards.

**Why this priority**: Configuration and booking are later expansion scope; booking requires a confirmed non-production Sandbox target and dedicated synthetic data.

**Independent Test**: With a fake browser, verify the fixed automation registry and trusted case metadata permit booking only on the approved Sandbox origin and reject all other origins before navigation.

**Acceptance Scenarios**:

1. **Given** pilot acceptance and owner confirmation of the Sandbox origin, **When** an approved booking automation is run, **Then** all destinations are checked against that exact origin before any navigation.
2. **Given** booking approval, dedicated accounts, or safe synthetic data is missing, **When** booking execution is requested, **Then** it remains disabled or is refused before browser launch.
3. **Given** a workbook title or step suggests a different journey or URL, **When** a booking case is dispatched, **Then** trusted metadata and the fixed registry—not editable text—determine its policy.

### Edge Cases

- Jira returns no stories, duplicate stories across pages, missing acceptance criteria, an inaccessible issue, a rate limit, malformed data, or a network/service error.
- JQL is malformed, broadens beyond the approved project or issue types, or attempts to access fields outside the approved retrieval scope.
- AI is disabled, unapproved, times out, returns malformed/incomplete structured data, or returns cases missing traceability.
- A workbook has invalid/missing headers, duplicate IDs, unsupported journeys/statuses, invalid Jira keys/links, malformed numbered steps, or unsafe overwrite/concurrent-edit conflicts.
- A case is Draft, Needs Update, Rejected, unmapped, not implemented, malformed, duplicated in a run selection, or has stale approval metadata.
- Environment configuration is missing, malformed, changed unexpectedly, uses credentials in the URL, points to production, uses a lookalike hostname, or specifies a disallowed port/scheme.
- A redirect changes origin; a browser is unavailable; a browser navigates before a policy check; or setup/cleanup fails.
- A booking case is requested for Staging, QA, PreProd, or an unknown environment, even if its title/steps claim the destination is Sandbox.
- The database or approved artifact store is unavailable, a concurrent user updates the same catalog, or a report write fails.
- Logs, errors, reports, screenshots, traces, or generated content could contain credentials, tokens, customer data, or payment data.
- The AI provider or organization has not approved sending Jira content, or Confluence functionality is requested without a separately approved scope.

## Requirements

### Functional Requirements

- **FR-001**: System MUST let an authorized user select Jira stories by issue key or an approved user-supplied JQL filter constrained to configured project and permitted issue types.
- **FR-002**: System MUST retrieve only approved Jira fields, preserve canonical issue keys and browse links, handle pagination, and report permission, rate-limit, network, empty-result, and missing-acceptance-criteria conditions explicitly.
- **FR-003**: System MUST keep Jira and Confluence integrations read-only by default and MUST NOT create or update remote issues, pages, comments, or attachments in this release.
- **FR-004**: System MUST support drafting positive, validation, and failure-path test scenarios for vehicle search, comparison, configuration, and booking, preserving source Jira traceability.
- **FR-005**: System MUST keep AI drafting disabled until the provider and Jira-content sharing have recorded organizational approval; it MUST send only the minimum approved content.
- **FR-006**: System MUST validate AI output against a strict structured schema and reject incomplete or malformed results rather than saving success-shaped cases.
- **FR-007**: System MUST represent each test case with case ID, Jira issue key/link, journey, title, priority, preconditions, numbered steps, expected results, test-data reference, review status, reviewer, review date, automation status, automation ID, and last result.
- **FR-008**: System MUST support Draft, Needs Update, Approved, and Rejected review states and MUST record reviewer and review date for review decisions.
- **FR-009**: System MUST never transition generated content to Approved without an explicit action by an authorized reviewer.
- **FR-010**: System MUST validate required catalog fields, unique case IDs, Jira keys/links, supported journey/status values, and numbered-step format, reporting actionable row and column errors.
- **FR-011**: System MUST support safe catalog import/export in Excel `.xlsx` format, validate before accepting writes, avoid overwriting populated data unless explicitly authorized, and protect against partial writes and concurrent-edit conflicts.
- **FR-012**: System MUST store persistent application records in PostgreSQL 15 and support repeatable, reviewable database migrations.
- **FR-013**: System MUST let a user select one or more case IDs and one of Staging, Sandbox, QA, or PreProd for an on-demand run.
- **FR-014**: System MUST display the selected environment and exact cases and require explicit confirmation before starting browser execution.
- **FR-015**: System MUST refuse Draft, Needs Update, Rejected, malformed, duplicate, unmapped, and non-implemented cases before browser launch, with actionable errors.
- **FR-016**: System MUST use a fixed registry mapping trusted automation IDs to implemented test functions and MUST NOT evaluate workbook text or dynamically import workbook-provided code.
- **FR-017**: System MUST enforce the configured exact-origin allowlist and hard production denial immediately before browser launch and every navigation, including redirect destinations.
- **FR-018**: System MUST enforce booking-only-on-approved-Sandbox using trusted journey/automation metadata, independent of selected environment and editable workbook content.
- **FR-019**: System MUST use dedicated test accounts and named synthetic test data with repeatable setup, cleanup, and reset procedures; it MUST NOT use real customer, payment, or production booking data.
- **FR-020**: System MUST run browser UI automation using the approved Python/pytest/Playwright runner and desktop Chrome, with a maintainable page-object/component structure and stable, application-approved selectors.
- **FR-021**: System MUST produce a unique run ID and record start/end time, selected cases, environment, browser, result totals, per-case outcomes, actionable failure details, and Jira links.
- **FR-022**: System MUST produce machine-readable run results and a concise human-readable summary in an approved destination, applying configured access and retention policies.
- **FR-023**: System MUST redact credentials, tokens, personal data, and payment data from logs and reports and MUST surface operational and safety-gate errors explicitly.
- **FR-024**: System MUST run the initial release on demand only; scheduled or automatic CI execution is out of scope unless the project scope is amended.
- **FR-025**: System MUST use React 18 with Vite for the team interface, Node.js with Express for the API, and Docker-managed PostgreSQL 15 for persistent application data.
- **FR-026**: The React client MUST communicate through the Express API and MUST NOT connect directly to PostgreSQL or contain Jira, Confluence, or AI-provider secrets.
- **FR-027**: The Express API MUST own external-service authentication, authorization checks, input validation, and persistence; shared API contracts MUST be explicit and validated at the boundary.
- **FR-028**: System MUST mock or isolate Jira, Confluence, AI-provider, browser, and database dependencies in the default automated suite; the suite MUST NOT require live credentials or contact production.
- **FR-029**: System MUST keep Confluence page retrieval or authoring disabled until a separately approved set of user needs, permitted fields/content, and access scope is defined. Any enabled access MUST be read-only by default.
- **FR-030**: System MUST provide clear setup and operational errors for missing configuration, unavailable environments, external-service failures, invalid catalog rows, and unavailable browser/runtime dependencies.

### Technology and Operational Constraints

- The user interface is React 18 with Vite; the API is Node.js with Express; the relational database is PostgreSQL 15 run through Docker for development.
- Browser automation remains a separate Python 3, pytest, and Playwright runner using desktop Chrome.
- Excel `.xlsx` remains a supported catalog exchange/template format. Whether it is also the authoritative shared catalog is unresolved.
- Jira integration is Jira Cloud REST and read-only for story retrieval in this release. Confluence has no functional retrieval or authoring requirements established in the source specification.
- Credentials MUST be provided through local environment variables or an approved secret manager. Committed configuration examples MUST contain placeholders only.
- PostgreSQL schema changes MUST use repeatable migrations. Docker images/configuration MUST pin PostgreSQL to major version 15 and MUST NOT commit real credentials.
- Browser targets are limited to explicitly approved Staging, Sandbox, QA, and PreProd origins. Production is prohibited; booking is Sandbox-only.
- Initial use is on-demand, browser-UI-only testing; GraphQL/API testing, scheduled/CI runs, and Jira writes are excluded.

### Key Entities

- **Jira Story**: An approved-scope Jira issue with canonical key, browse link, and permitted description/acceptance-criteria fields.
- **Test Case**: A uniquely identified, Jira-traceable scenario with journey, priority, preconditions, numbered steps, expected results, test-data reference, review metadata, automation mapping, and latest result.
- **Catalog**: A validated collection of test cases that can be represented in an Excel workbook and maintained by the QA team.
- **Review Decision**: A transition to Draft, Needs Update, Approved, or Rejected, attributed to an authorized reviewer and review date.
- **Automation Mapping**: A trusted registry entry linking an automation ID to an implemented browser test and its policy metadata, including booking classification.
- **Environment Configuration**: An approved environment name and canonical base origin, with production denial and a Sandbox designation for booking.
- **Run**: A user-confirmed on-demand execution with a unique ID, initiator, environment, browser, selected cases, timestamps, totals, and summary destination.
- **Case Result**: A per-case pass/fail/skip outcome, actionable failure details, and source Jira traceability associated with a run.
- **Test Data Fixture**: Named synthetic data and setup/cleanup/reset behavior used to make execution repeatable.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every saved generated test case retains a valid source Jira key/link and starts in Draft; automated tests verify both properties.
- **SC-002**: Every invalid, unapproved, duplicate, unmapped, non-implemented, or unconfirmed run is refused before browser launch; the fake-browser navigation count is zero.
- **SC-003**: Automated environment tests demonstrate that no production, lookalike, malformed, unapproved-origin, or unsafe-redirect URL is navigated to.
- **SC-004**: Automated booking-policy tests demonstrate that booking cases navigate only to the approved Sandbox origin across all supported general environment selections and representative edited-workbook cases.
- **SC-005**: Every completed run has a unique run ID and all required run metadata, case outcomes, totals, actionable failures, and Jira links; tests verify totals agree with per-case results.
- **SC-006**: Catalog validation identifies invalid entries by row and column and preserves the previous valid catalog after failed validation or write.
- **SC-007**: The default automated suite completes without Jira, Confluence, or AI credentials and without contacting production or external Vehicle Shop environments.
- **SC-008**: Jira and Confluence test doubles verify no remote write operation is issued by the initial release.
- **SC-009**: Concurrent catalog edits or result writes do not silently overwrite another user's data; conflicts are reported for resolution.
- **SC-010**: Pilot acceptance verifies approved URLs, production blocking, Sandbox-only booking policy, synthetic data, secret redaction, explicit run confirmation, and run-summary traceability before expanding coverage.

## Assumptions

- The primary users are a QA lead and a team of 10 QA members; the initial pilot focuses on vehicle search and comparison.
- Story selection is limited to the configured Jira Cloud project and owner-approved issue types/fields. The backlog proposes project key `PROJECTCARS` and a starting JQL, but owner confirmation is still required.
- The application uses PostgreSQL 15 for persistent records because that is mandated by the project constitution. Excel remains an import/export format; **whether Excel or PostgreSQL is the authoritative shared catalog requires confirmation**.
- The initial runner is on-demand and browser-UI-only. The React interface may coordinate the workflow but must not weaken runner-side safety checks.
- AI-assisted case drafting is unavailable until an approved provider and data-sharing policy are confirmed. Manual case authoring/editing remains possible.
- Confluence automation is not defined by the source Vehicle Shop specification. Confluence features are therefore excluded from this feature's functional scope until separate requirements and permissions are approved.
- **[NEEDS CLARIFICATION: Environment owners must supply canonical base URLs and confirm which of Staging, Sandbox, QA, and PreProd are in the pilot.]**
- **[NEEDS CLARIFICATION: Confirm the Jira base URL, project key, read permissions, permitted issue types/fields, and approved JQL filter.]**
- **[NEEDS CLARIFICATION: Identify the approved AI provider and approve or prohibit sending the minimum required Jira story content.]**
- **[NEEDS CLARIFICATION: Define application authentication/authorization, authorized reviewers and run initiators, and how reviewer identity is verified.]**
- **[NEEDS CLARIFICATION: Confirm whether the Excel workbook or PostgreSQL is the source of truth, where the team shares catalogs, and how concurrent edits/version recovery work.]**
- **[NEEDS CLARIFICATION: Define approved run-summary/artifact storage, access controls, retention period, and whether screenshots/traces are allowed or required.]**
- **[NEEDS CLARIFICATION: Confirm dedicated test-account provisioning, login steps, synthetic data setup/reset/cleanup, and exactly which Sandbox booking/payment behaviors are safe.]**
- **[NEEDS CLARIFICATION: Confirm supported desktop Chrome version and operating systems for the pilot.]**
- **[NEEDS CLARIFICATION: Define the objective production-target denial criteria in addition to the allowlist, and confirm the owner-approved Sandbox origin is non-production.]**
- **[NEEDS CLARIFICATION: Define pilot exit/acceptance authority and required evidence before enabling configuration and booking automation.]**
