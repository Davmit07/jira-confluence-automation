# TODO

## Phase 1 - Foundation

### Completed
- [x] Confirm scope: Jira stories, browser UI only, desktop Chrome, Excel catalog, and on-demand runs.
- [x] Confirm environment names: Staging, Sandbox, QA, and PreProd; booking tests are Sandbox-only.
- [x] Define test-case fields and Jira traceability columns in `project_spec.md`.
- [x] Create and verify `test-cases-template.xlsx` with Jira traceability, review date, and field dropdowns.
- [x] Add `openpyxl` to `requirements.txt` and install it in the ignored `.venv`.

### Needs input or configuration
- [ ] Confirm the story filter and read permissions, then configure a newly rotated Jira token locally. Project key provided: `PROJECTCARS`; account access identified as EPAM, but local token setup is unverified.
- [ ] Validate this proposed pilot JQL in Jira: `project = PROJECTCARS AND issuetype = Story AND statusCategory != Done ORDER BY priority DESC, updated DESC`.
- [ ] Provide Vehicle Shop base URLs and login flow; confirm supported Chrome/OS versions and which environments are in the first pilot.
- [ ] Define dedicated test accounts, test-data setup/reset, and safe Sandbox booking/payment behavior.
- [ ] Choose shared Excel catalog storage and a process for concurrent edits by the 10-person team.
- [ ] Select an organization-approved AI provider and confirm whether Jira story content may be sent to it. No provider is approved yet; do not send Jira content to an AI service.
- [ ] Name or identify who can review/approve cases and start runs.
- [ ] Decide where run summaries, screenshots, and traces are stored and how long they are retained.
- [ ] Decide whether failures may create Jira bugs or only appear in reports.
- [ ] Populate and verify the environment URL allowlist; production URLs must remain blocked.

## Later phases
- [ ] Build the Jira story-to-draft workflow with human review before approval.
- [ ] Implement approved-case execution with Python, pytest, and Playwright for desktop Chrome.
- [ ] Pilot search and comparison cases in Sandbox, then expand to configuration and bookings.
