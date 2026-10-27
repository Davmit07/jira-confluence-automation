# Specification Implementation Checklist

**Baseline:** [`specification.md`](./specification.md), Draft as of 2026-10-27
**Assessment date:** 2026-10-27
**Scope:** Current files and runtime behavior in this repository; a scaffold, placeholder, or isolated demonstration is not treated as an implemented end-to-end feature.

## Assessment Summary

The project currently has useful foundations, but the specified Jira-to-test-result workflow is not implemented. The API exposes only a health check, the React page is a static setup preview with workflow controls disabled, and PostgreSQL is running without application tables, migrations, or an API connection. Existing Python workbook utilities provide schema/catalog generation and validation; a separate candy-purchase simulator tests some safety logic but is not a Vehicle Shop browser runner.

| Area | Implementation | Working evidence |
|---|---|---|
| React 18/Vite preview | Partial | Vite production build succeeds; dev page responds HTTP 200. No workflow integration or UI behavior tests. |
| Express API | Partial | `GET /health` responds HTTP 200 and its Node test passes. No application routes or persistence. |
| PostgreSQL 15 | Partial | Docker Compose service is healthy and `SELECT 1` succeeds. No application schema, migrations, or API connection. |
| Excel catalog utilities | Partial | Schema generation and validation tests pass; no integrated import/review/persistence workflow. |
| Jira, AI, and Confluence features | Not implemented | No application integration is present. No external credentials or services are used by the current app. |
| Vehicle Shop browser execution and reporting | Not implemented | No Vehicle Shop Playwright runner or run-summary workflow. Candy simulator is isolated and uses a fake browser. |
| Pilot approvals and environment policy | Not complete | Staging and search/compare-only are proposals; canonical origins, production-denial source/criteria, and owner sign-off remain unresolved. |

**Evidence limitation:** the Python unittest suite ran 38 tests: 37 passed and one test module failed to import. `test_define_catalog_schema.py` points to a nonexistent `tools/define-corepy`; the repository contains `tools/define-core.py`. Therefore, the full Python suite is not green.

## Status Definitions

- **Implementation — Implemented:** the requirement is present in the intended application path.
- **Implementation — Partial:** only a subset, utility, prototype, or isolated demonstration exists.
- **Implementation — Not implemented:** no relevant implementation exists.
- **Works — Verified:** direct runtime check or test exercises the requirement.
- **Works — Partially verified:** evidence covers a narrower utility/demo, not the specified application behavior.
- **Works — Not verified:** the feature is absent or there is no evidence it works.
- **Works — Fails:** the attempted check failed. The Python-suite import failure is recorded separately from the functional feature statuses.

## User Stories and Acceptance Scenarios

Each acceptance scenario is assessed separately. “Partial” refers to isolated workbook utilities or the candy simulator, not completion of the application workflow.

| Story / scenario | Implementation | Works | Evidence / gap |
|---|---|---|---|
| US-1 AC1: retrieve an authorized Jira story and canonical fields/link | Not implemented | Not verified | No Jira client or API route. |
| US-1 AC2: search approved JQL with pagination and no writes | Not implemented | Not verified | No Jira search or pagination. |
| US-1 AC3: validate AI draft output and save traceable Draft cases | Not implemented | Not verified | No AI provider/adapter or app authoring path. |
| US-1 AC4: explain that unapproved AI drafting is disabled | Partial | Partially verified | No AI integration or send path exists, but there is no explicit AI approval state or explanatory drafting UI. |
| US-1 AC5: report missing acceptance criteria without creating false-success cases | Not implemented | Not verified | No story retrieval/drafting path. |
| US-2 AC1: display/export required case fields and Jira traceability | Partial | Partially verified | Workbook schema/generation utilities exist; no application catalog display/export workflow. |
| US-2 AC2: authorized review transitions with reviewer/date | Partial | Partially verified | Catalog fields and validation exist; there is no transition service or reviewer authorization. |
| US-2 AC3: never auto-approve generated/edited cases | Partial | Partially verified | Generators initialize cases as Draft; there is no application review lifecycle enforcing this rule. |
| US-2 AC4: validate workbook errors by row/column | Implemented | Verified for the validator utility | Validator tests cover malformed headers, fields, Jira references, duplicates, steps, and actionable errors. |
| US-2 AC5: preserve catalog after invalid write or concurrent conflict | Partial | Partially verified | Generator tests cover protected/atomic output cases; there is no shared catalog update or concurrent-edit workflow. |
| US-3 AC1: show environment and exact case IDs before run | Not implemented | Not verified | No run-selection workflow; preview controls are disabled. |
| US-3 AC2: cancellation/unconfirmed run causes zero navigation | Not implemented | Not verified | No application run confirmation/submission path. |
| US-3 AC3: reject invalid/unapproved/unmapped cases before launch | Partial | Partially verified | Candy simulator rejects an unknown automation ID; it does not validate Vehicle Shop catalog status or launch a real browser. |
| US-3 AC4: enforce approved origins and production denial before navigation | Partial | Partially verified | Candy simulator has exact-origin and redirect checks; there is no Vehicle Shop environment allowlist or independent production policy. |
| US-3 AC5: booking policy comes from trusted metadata, not workbook text | Partial | Partially verified | Candy simulation is Sandbox-only, but it does not dispatch Vehicle Shop booking cases through a trusted registry. |
| US-3 AC6: attempt cleanup and record failures without sensitive data | Not implemented | Not verified | No browser lifecycle, fixture cleanup, or run failure reporting. |
| US-4 AC1: persist complete run metadata and per-case outcomes | Not implemented | Not verified | No run model or result persistence. |
| US-4 AC2: actionable, redacted failure details | Not implemented | Not verified | No run reports or redaction path. |
| US-4 AC3: produce approved machine/human-readable outputs | Not implemented | Not verified | No run output workflow. |
| US-4 AC4: report failures without Jira writes | Partial | Partially verified | No Jira write integration exists, but there is no run failure path or integration test double. |
| US-5 AC1: run approved search/compare UI cases and record results | Not implemented | Not verified | No Vehicle Shop Playwright cases, approved origin, or run workflow. |
| US-5 AC2: cleanup synthetic state after failures | Not implemented | Not verified | No Vehicle Shop browser fixtures or cleanup hooks. |
| US-5 AC3: block runs and identify missing pilot prerequisites | Not implemented | Not verified | No run-preflight workflow. The known approvals/origin remain unresolved. |
| US-6 AC1: validate every booking destination against approved Sandbox | Partial | Partially verified | Candy simulator tests same-origin destinations with a fake browser; no approved Vehicle Shop Sandbox origin or booking runner exists. |
| US-6 AC2: keep booking disabled without approvals/accounts/data | Partial | Partially verified | No Vehicle Shop booking feature is exposed, but there is no explicit booking gate or prerequisite explanation. |
| US-6 AC3: derive booking policy from trusted metadata, not editable text | Partial | Partially verified | Toy simulator uses a fixed automation ID; no Vehicle Shop registry or dispatch path exists. |

## Functional Requirements

| ID | Implementation | Works | Evidence / gap |
|---|---|---|---|
| FR-001 | Not implemented | Not verified | No authorized Jira story selection by key or JQL. |
| FR-002 | Not implemented | Not verified | No Jira retrieval, approved-field filtering, pagination, or Jira error handling. |
| FR-003 | Partial | Partially verified | No Jira/Confluence integrations or remote-write path exist, so writes are currently impossible; read-only policy enforcement and tests are absent. |
| FR-004 | Partial | Partially verified | Python utilities create traceable Draft workbook rows from supplied/synthetic inputs, but not Jira-derived scenario drafts. The shop-catalog generator includes configuration and booking examples; the proposed search/compare-only pilot boundary is not enforced across authoring/review/mapping/execution. |
| FR-005 | Partial | Partially verified | No AI integration can send content, but there is no provider approval state or explicit disabled-with-reason drafting workflow. |
| FR-006 | Not implemented | Not verified | No AI response schema validation. |
| FR-007 | Partial | Partially verified | The Excel schema represents catalog fields, but there is no application domain model or persistent catalog API. |
| FR-008 | Partial | Partially verified | Validator accepts/checks review values and reviewer/date requirements; no state-transition or authorized-review service exists. |
| FR-009 | Partial | Partially verified | Catalog generators initialize Draft rows; no application workflow enforces explicit authorized approval. |
| FR-010 | Implemented in catalog utility | Verified for the validator utility | Validator tests cover required fields, case-ID uniqueness, Jira key/link checks, enum values, numbered steps, and row/column errors. |
| FR-011 | Partial | Partially verified | `.xlsx` generation and validation exist, including overwrite/failed-output protections in generator tests. Integrated import, validated catalog writes, and concurrent-edit conflict resolution do not. |
| FR-012 | Partial | Partially verified | PostgreSQL 15 runs in Docker and accepts a SQL query; no application records, schema, migrations, or API database connection exist. |
| FR-013 | Not implemented | Not verified | No case/environment run selector. |
| FR-014 | Not implemented | Not verified | No exact-selection confirmation or browser execution control. |
| FR-015 | Partial | Partially verified | The candy demo refuses an unknown ID and unsafe environment before fake navigation; it does not preflight Vehicle Shop case status, duplicates, mapping, or browser launch. |
| FR-016 | Partial | Partially verified | Candy demo uses one fixed ID, but there is no general registry mapping approved Vehicle Shop IDs to implemented browser tests. No application path interprets workbook text as code. |
| FR-017 | Partial | Partially verified | Exact-origin and redirect checks are tested in the isolated candy simulator only. Vehicle Shop origins, independent production denial, and browser-navigation enforcement are absent. |
| FR-018 | Partial | Partially verified | The candy simulator is restricted to its synthetic Sandbox origin. No Vehicle Shop booking case, trusted journey metadata, or approved Sandbox configuration exists. |
| FR-019 | Not implemented | Not verified | No dedicated Vehicle Shop accounts, named test fixtures, or repeatable setup/reset/cleanup. |
| FR-020 | Not implemented | Not verified | Python catalog tools and a fake-browser simulator exist, but no pytest/Playwright desktop-Chrome Vehicle Shop runner, page objects, or selectors. |
| FR-021 | Not implemented | Not verified | No run IDs, run metadata, case outcomes, or result totals. |
| FR-022 | Not implemented | Not verified | No machine-readable or human-readable run summary or approved artifact destination. |
| FR-023 | Partial | Partially verified | Catalog validation surfaces row/column errors and a local DB secret is kept out of Git; there is no application logging/reporting redaction or complete operational-error handling. |
| FR-024 | Partial | Not verified | No run capability exists, and no scheduled/CI run path was found. The “on-demand only” behavior cannot be validated until runs exist. |
| FR-025 | Partial | Partially verified | React 18/Vite, Node/Express, and Docker PostgreSQL 15 components exist independently. Only the API health endpoint works; the stack is not integrated for persistent application data. |
| FR-026 | Partial | Partially verified | The web page does not connect to Express, PostgreSQL, or external providers. Thus direct DB access/secrets are not present, but required client-to-API workflows are also absent. |
| FR-027 | Not implemented | Not verified | The API has no application auth, authorization, input validation, persistence, or shared contract boundary. |
| FR-028 | Partial | Partially verified | Local utility/API tests do not require live service credentials; there are no Jira, Confluence, AI, browser, or application-database integration doubles. The current Python suite has one import error. |
| FR-029 | Implemented as absent/disabled capability | Verified by implementation inventory | No Confluence retrieval or authoring feature exists. No approved Confluence capability has been enabled. |
| FR-030 | Partial | Partially verified | Catalog validation has explicit actionable errors. API/configuration, environment, external-service, and browser/runtime operational errors are not implemented. |

## Success Criteria

| ID | Implementation | Works | Evidence / gap |
|---|---|---|---|
| SC-001 | Partial | Partially verified | Workbook utilities create Draft rows with Jira fields, but the criterion is not exercised on Jira-retrieved story drafts; no end-to-end app test. |
| SC-002 | Partial | Partially verified | Candy tests assert zero fake-browser navigation for invalid toy cases/configuration; no Vehicle Shop preflight or browser-launch boundary. |
| SC-003 | Partial | Partially verified | Candy URL tests reject unsafe origins/redirects; no approved Vehicle Shop origin list or independent production-denial tests. |
| SC-004 | Partial | Partially verified | Candy simulator tests Sandbox-only simulated purchase behavior; it does not exercise Vehicle Shop booking metadata/flows. |
| SC-005 | Not implemented | Not verified | No run record, required metadata, case results, or totals. |
| SC-006 | Partial | Partially verified | Validator identifies row/column errors; catalog utilities test protection against failed/unsafe output. No integrated import/update transaction or concurrency workflow. |
| SC-007 | Partial | Fails | Tests do not require live Jira/AI credentials, but `unittest discover -s tests -v` completed with 37 passing tests and one import error caused by the stale `tools/define-corepy` path. |
| SC-008 | Partial | Partially verified | No remote integrations/writes are implemented, but required Jira/Confluence test doubles verifying no writes are absent. |
| SC-009 | Not implemented | Not verified | No shared concurrent catalog/result persistence or conflict resolution. |
| SC-010 | Not implemented | Not verified | No completed safety acceptance package or recorded go/no-go sign-off; environment and pilot approvals remain pending. |

## Technology and Operational Constraints

| Constraint | Implementation | Works | Evidence / gap |
|---|---|---|---|
| React 18 and Vite interface | Partial | Partially verified | React/Vite dependencies and static preview exist; production build succeeds. No workflow/API integration. |
| Node.js and Express API | Partial | Partially verified | Express `/health` endpoint responds successfully; API unit test passes. No product routes. |
| PostgreSQL 15 via Docker for app persistence | Partial | Partially verified | Compose database is healthy and `SELECT 1` returns `1`; no app tables, migrations, or app connection. |
| Python 3, pytest, Playwright, desktop Chrome runner | Not implemented | Not verified | Python utilities and a fake-browser simulator are not a Playwright runner; no Vehicle Shop browser cases. |
| Excel `.xlsx` exchange/template | Partial | Partially verified | Schema/generator/validator utilities and related tests exist; no integrated import/export lifecycle. |
| Jira Cloud, read-only story retrieval | Not implemented | Not verified | No application Jira client or story retrieval. |
| AI drafting behind provider/data approval | Partial | Partially verified | No AI calls are possible, but no provider-neutral adapter or approval control exists. |
| Local environment variables/approved secret manager; placeholders only in committed examples | Partial | Partially verified | No external-service credentials are configured in the app; PostgreSQL local secret is ignored by Git. No complete application secret/configuration workflow. |
| Repeatable PostgreSQL migrations | Not implemented | Not verified | No migration files or migration runner found. |
| Approved-origin allowlist, production denial, Sandbox-only booking | Partial | Partially verified | Toy candy simulator covers a narrow exact-origin/Sandbox policy; no Vehicle Shop policy configuration or production-target rule. |
| On-demand, browser-UI-only; no API/GraphQL tests, scheduled/CI runs, or Jira writes | Partial | Not verified | No browser run path or scheduled run found. No Jira write path exists because Jira integration is absent. |
| Confluence disabled until separate approval | Implemented as absent/disabled capability | Verified by implementation inventory | No Confluence code or UI capability is present. |
| Pilot limited to search and comparison; configuration and booking deferred | Partial | Partially verified | The React preview exposes no journey workflow, but the catalog generator can create configuration/booking examples; lifecycle gating is not enforced. Owner sign-off is still pending. |

## Verification Performed

| Check | Result | What it establishes |
|---|---|---|
| API `npm test` in `apps/api` | Pass: 1 test | The health route test passes. |
| `GET http://127.0.0.1:3000/health` | Pass: HTTP 200, `{"status":"ok"}` | The running Express health endpoint responds. |
| Frontend `npm run build` in `apps/web` | Pass | Vite creates a production bundle. |
| Frontend `npm audit` | Pass: 0 vulnerabilities | The installed frontend dependency tree has no reported audit findings. |
| `GET http://127.0.0.1:5173/` | Pass: HTTP 200 | The running preview server serves a page; this is not an end-to-end workflow test. |
| Python `unittest discover -s tests -v` with project virtual environment | Incomplete: 37 passed, 1 import error | Catalog and candy tests that loaded passed; `test_define_catalog_schema` could not import due to the stale path `tools/define-corepy` (the present tool is `tools/define-core.py`). |
| Docker Compose PostgreSQL health | Pass: healthy | PostgreSQL 15 container is running and reports healthy. |
| `SELECT 1` against `vehicle_shop` database | Pass: returned `1` | The database accepts a local SQL connection; it does not verify application persistence. |

## Outstanding Gaps and Readiness

1. Complete stakeholder decisions and approvals before any browser execution: canonical Staging origin, production-denial source and criteria, browser enforcement boundary, approved non-production Sandbox origin, pilot scope sign-off, and acceptance authority.
2. Fix the test discovery/import path mismatch and rerun the complete Python suite.
3. Implement an application data model, PostgreSQL migrations, and Express persistence/API contracts.
4. Implement Jira retrieval, the catalog authoring/review workflow, explicit user authorization, and pilot lifecycle restrictions.
5. Implement a fixed Vehicle Shop automation registry and a real pytest/Playwright runner only after environment, account, and synthetic-data approvals.
6. Add run confirmation, safety preflight, exact-origin/production gates at navigation time, and Sandbox-only trusted booking policy before any browser launch.
7. Implement run records, redacted outputs, concurrency handling, and an approved report destination.
8. Add automated tests for integrated application behavior and safety boundaries. The current passing helper tests do not establish end-to-end compliance.

**Release assessment:** Not ready for a functional pilot. Current work is a foundation/scaffold and isolated utility coverage; the unresolved approval gates and absent integrated workflow prevent the specified product from being exercised safely or end to end.
