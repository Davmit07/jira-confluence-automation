# Project Constitution

This constitution defines the non-negotiable principles for the Jira/Confluence automation project. It governs design, implementation, review, testing, and operation. If a change conflicts with a principle, revise the change or amend this constitution before proceeding.

## Core Principles

### I. Human Approval and Traceability
- Every generated test case MUST remain a draft until an authorized QA reviewer explicitly approves it.
- Test cases and execution results MUST retain their originating Jira issue key and canonical link.
- Approval, review date, run initiator, selected cases, environment, and per-case outcomes MUST be attributable and recorded.
- The system MUST require explicit user confirmation before starting an execution run.

### II. Safe, Least-Privilege Integrations
- Jira and Confluence credentials MUST be supplied through local environment configuration or an approved secret manager; credentials MUST NOT be committed or included in workbooks, reports, browser storage, or logs.
- External integrations MUST request only the permissions and data required for the approved feature.
- Jira and Confluence access MUST be read-only by default. Creating or updating issues, pages, comments, attachments, or other remote content requires explicit scope approval and a separately reviewed implementation.
- AI-provider integration MUST remain disabled until an organization-approved provider and data-sharing approval are recorded. Only the minimum approved content may be sent.

### III. Environment and Execution Safety
- Browser automation MUST use an explicit allowlist of canonical environment origins and MUST reject malformed URLs, unapproved origins, unsafe redirects, and production targets before navigation.
- Booking automation MUST run only against the approved Sandbox origin, regardless of the user's general environment selection or editable workbook text.
- Execution MUST dispatch through a fixed registry of implemented automation identifiers. Workbook content MUST never be evaluated as code or used to dynamically import executable logic.
- Tests and demonstrations MUST use synthetic data and dedicated test accounts; real customer, payment, and production booking data are prohibited.

### IV. Reviewable, Reproducible Results
- Catalog validation MUST report actionable row/column errors and preserve the source catalog data unless an overwrite is explicitly requested.
- Runs MUST record a unique run ID, timestamps, environment, browser, selected cases, result totals, per-case outcomes, actionable failures, and Jira traceability.
- Run outputs MUST be stored only in approved locations and MUST follow configured access and retention policies.
- Failures MUST be surfaced clearly; the system MUST NOT silently skip required work or report success-shaped fallbacks.

### V. Test-First Safety and Quality
- Safety rules, state transitions, integration behavior, and error paths MUST have deterministic automated tests.
- External Jira, Confluence, AI, and browser behavior MUST be mocked or isolated in the default test suite; tests MUST NOT require live credentials or contact production.
- Changes MUST include focused tests and documentation updates for affected user workflows.
- The default execution model is on-demand browser UI testing. Scheduled/CI execution and API/GraphQL testing are out of scope unless the project scope is explicitly amended.

### VI. Approved Technology Baseline
- The team interface MUST use React 18 with Vite.
- The application backend MUST use Node.js with Express.
- Persistent application data MUST use PostgreSQL 15, run locally or in development through Docker.
- Browser UI automation MUST remain in the existing Python/pytest/Playwright runner unless an approved architecture change replaces it.
- Dependencies and container images MUST be versioned or constrained to the approved major versions; upgrades require compatible tests and review.

## Architecture and Data Boundaries

- The React client MUST call the Express API and MUST NOT connect directly to PostgreSQL or contain Jira, Confluence, or AI-provider secrets.
- The Express API MUST own authentication to external services, authorization checks, input validation, and persistence.
- Shared request/response contracts MUST be explicit and validated at the API boundary.
- PostgreSQL schema changes MUST use reviewable, repeatable migrations; production data MUST NOT be used for local or automated tests.
- Docker configuration MUST pin PostgreSQL to major version 15 and MUST avoid embedding credentials in committed files. Example configuration MUST use placeholders only.

## Governance

- A change that violates or weakens a principle MUST NOT proceed without first updating this constitution through review.
- Amendments MUST state the affected principle, rationale, risks, and migration or validation plan.
- Code review MUST verify the change against applicable principles and include evidence from focused tests.
- This constitution takes precedence over conflicting project conventions. More specific feature requirements may add safeguards but MUST NOT weaken these principles without an approved amendment.
