# Vehicle Shop Test Case Automation: Technical Specification

## 1. Purpose

Provide a reviewable workflow for turning Jira stories into test cases, maintaining an Excel test catalog, running approved browser tests on demand, and reporting results and Jira traceability for the Vehicle Shop project.

## 2. Users and Scope (Pilot Boundary Proposed; Approval Pending)

- Primary user: QA lead managing a team of 10.
- Test authoring input: Jira stories and their acceptance criteria.
- Test surface: browser UI only; GraphQL/API testing is not in scope.
- Product boundary: this Vehicle Shop Jira test-automation feature belongs to the broader Jira/Confluence automation project; it does not define a complete Confluence feature. Confluence access is disabled and out of scope for this release unless separately approved.
- Product journeys across the roadmap: search vehicles, compare vehicles, configure vehicles, and bookings.
- Proposed initial-pilot boundary: only search and comparison cases may be authored, reviewed, approved, mapped, and executed. Configuration and booking are deferred from all pilot lifecycle stages and require a later scope decision; booking additionally requires separate Sandbox safety approval.
- Target browser: desktop Chrome with internet access.
- Candidate test environments: Staging, Sandbox, QA, and PreProd. Staging is the proposed initial pilot environment pending application/environment-owner approval; no valid canonical origin has been supplied. Production-denial criteria, URL/browser enforcement boundary, and the owner-confirmed non-production Sandbox origin remain unresolved. No browser execution or booking is authorized until the applicable policy and environment approvals are recorded. Bookings must use Sandbox only.
- Test case catalog: Excel workbook (`.xlsx`), using a template defined by the solution.
- Run mode: on demand; no scheduled or automatic CI runs in the initial scope.
- Generation and execution results require Jira traceability.
- Test cases are drafts until a QA owner reviews and approves them.
- Required run outputs: pass/fail results and a summary.
- Existing test-management and automation tools: none specified.
- Proposed pilot acceptance authority: QA lead together with product and environment owners. Proposed evidence: test results, safety checklist, known limitations, and a recorded go/no-go sign-off. Product-owner and QA-lead approval remains pending; no pilot environment selection is made here.

## 3. Proposed Workflow

1. Select Jira stories by project, filter, or issue key.
2. Read story descriptions and acceptance criteria; during the initial pilot, create candidate cases only for vehicle search and comparison. AI use remains subject to separate provider and data-sharing approval.
3. Save candidates to the Excel catalog with their Jira issue links and draft status.
4. A QA owner reviews, edits, and approves cases. Only approved cases with an automation mapping can run.
5. A user selects approved cases and an allowed environment, then starts a run on demand.
6. The runner executes browser tests in desktop Chrome and records results against case IDs and Jira stories.
7. Produce a run summary with pass/fail totals, failures, and Jira traceability.

## 4. Functional Requirements

- **FR-1 Story selection:** Retrieve Jira stories and acceptance criteria using a configured project and user-selected filter or issue keys.
- **FR-2 Draft generation:** Produce candidate scenarios covering positive paths, relevant validation, and failure paths for journeys enabled in the active release phase. During the initial pilot, authoring is limited to search and comparison; configuration and booking are deferred from all pilot lifecycle stages. Generated content must retain its source Jira issue key and must not be treated as approved automatically.
- **FR-3 Human review:** Support draft, approved, rejected, and needs-update states, plus reviewer and review date.
- **FR-4 Excel catalog:** Store one test case per row. Include: case ID, Jira issue key/link, journey, title, priority, preconditions, numbered steps, expected results, test-data reference, review status, reviewer, automation status, automation ID, and last result.
- **FR-5 Browser automation:** Use a maintainable page-object/component model and stable UI selectors. Execute only approved cases that have an implemented automation ID; do not attempt to interpret arbitrary spreadsheet text as executable code.
- **FR-6 On-demand run:** Allow a user to select cases and one of Staging, Sandbox, QA, or PreProd before execution. Require explicit confirmation before starting a run.
- **FR-7 Run summary:** Record run ID, start/end time, environment, browser, selected case IDs, pass/fail/skip counts, per-case results, and Jira links. Provide actionable failure details; screenshots or traces are a proposed enhancement pending confirmation.
- **FR-8 Traceability:** Preserve links from each case and result to its source Jira story. Creating or updating Jira issues from failures is not included unless approved later.
- **FR-9 Repeatability:** Use named test data and cleanup/reset steps so cases can be rerun without depending on prior test state.

## 5. Booking and Environment Safeguards

- Booking flows may run only against the Sandbox environment, regardless of the environment selected for other cases.
- Block production URLs and require an allowlist of approved environment base URLs.
- Use dedicated test accounts and sandbox booking data; do not use real customer or payment information.
- Stop a run if the target URL cannot be matched to an approved environment or if a booking test is directed outside Sandbox.
- Keep credentials and tokens out of the workbook, generated reports, source control, and logs.

## 6. Recommended Technical Approach

- **Language and runner:** Python 3 with pytest.
- **Browser automation:** Playwright for Python, configured for desktop Chrome.
- **Workbook handling:** `openpyxl` for reading and writing the Excel catalog.
- **Jira integration:** Jira Cloud REST API, read-only for story retrieval and traceability by default.
- **AI integration:** Provider-neutral adapter for drafting test cases. Select an approved provider and confirm data-handling rules before implementation; send only the minimum story content required.
- **Configuration:** Local environment variables or a secret manager. Never commit API tokens or credentials.
- **Execution interface:** Use the approved React 18/Vite team interface through the Node.js/Express API for catalog and run workflows; preserve the separately governed Python/pytest/Playwright runner. Do not treat the earlier CLI-first recommendation as the release architecture.
- **Reporting:** Generate a machine-readable result file and a concise Markdown/HTML summary; exact destination remains to be confirmed.

## 7. Non-Functional Requirements

- Support concurrent use by a 10-person QA team without overwriting another user's workbook or run results.
- Make runs reproducible through versioned test definitions, environment selection, and recorded run metadata.
- Provide clear errors for Jira access failures, missing acceptance criteria, invalid workbook rows, and unavailable environments.
- Keep generated tests reviewable and editable; log who approved cases and initiated runs.
- Avoid logging secrets or sensitive personal data, and apply the organization's retention policy to run artifacts.

## 8. Acceptance Criteria

- A QA user can select Jira stories and generate draft cases that preserve Jira links.
- Draft cases can be reviewed and maintained in the defined Excel template.
- The runner refuses draft, rejected, or unmapped cases.
- A QA user can run approved mapped cases on demand in desktop Chrome against an allowlisted environment.
- Booking cases are blocked unless the target is the approved Sandbox URL.
- Each run produces a summary with pass/fail totals and per-case Jira traceability.
- No live payment, production booking, or unapproved environment is contacted during a run.

## 9. Open Questions

- What are the Jira project key, issue filter, and account permissions for reading stories?
- What are the Vehicle Shop URLs, login flow, supported Chrome/OS versions, and available test accounts?
- How are test data created, reset, and cleaned up? Which sandbox booking/payment behavior is safe to exercise?
- Where should the shared `.xlsx` catalog live, and how should concurrent edits be handled?
- Which AI provider is approved, and may Jira story content be sent to it?
- How should QA approval be recorded, and who may approve cases or start runs?
- Should screenshots/traces be required, and where should run summaries and artifacts be stored and retained?
- Should failures only appear in reports, or may the solution create Jira bugs in a later phase?
- Are Staging, QA, and PreProd all required for the first release, or should the pilot start with Sandbox only?

## 10. Delivery Phases

- **Phase 1 - Foundation:** Confirm open questions, define the workbook, environment allowlist, Jira access, and approved AI provider.
- **Phase 2 - Pilot:** Author, review, approve, map, and execute only vehicle search and comparison cases. The pilot environment is not selected by this scope decision and requires owner approval.
- **Phase 3 - Expand:** Add configuration and sandbox booking flows, broaden coverage, and validate reporting with the full QA team.
- **Phase 4 - Adopt:** Review quality and team feedback before considering CI triggers, additional browsers, or automated Jira bug creation. The React/Express team interface is part of the approved application baseline, not a post-pilot option.