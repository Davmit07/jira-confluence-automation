# Module 10 Completion Report

## Instruction Files
```text
instructions/add-catalog-validation.agent.md
instructions/create-status-report.agent.md
instructions/creating-instructions.agent.md
instructions/implement-secure-jira-authentication.agent.md
instructions/main.agent.md
instructions/test-booking-sandbox-enforcement.agent.md
instructions/work-on-vehicle-shop-test-automation.agent.md
```

## main.agent.md Contents
```markdown
# Instructions Catalog

Load the relevant instruction completely before acting. Use the keywords and targets below to route requests.

- [`./create-status-report.agent.md`](./create-status-report.agent.md) — Create concise weekly status reports using verified project information.
  + Keywords: status report, weekly update, team update, accomplishments, blockers, next week
- [`./work-on-vehicle-shop-test-automation.agent.md`](./work-on-vehicle-shop-test-automation.agent.md) — Implement and maintain the Vehicle Shop test-case automation project within its defined safety and scope limits.
  + Keywords: Vehicle Shop, test automation, test catalog, Jira stories, Playwright, Sandbox
  + Target: `work/module03-task/**`
- [`./add-catalog-validation.agent.md`](./add-catalog-validation.agent.md) — Implement validation for Jira-traceable Excel test catalogs and report actionable row/column errors.
  + Keywords: catalog validation, validate workbook, Excel validation, test-case rows, Jira key, numbered steps
  + Target: `work/module03-task/**`
- [`./implement-secure-jira-authentication.agent.md`](./implement-secure-jira-authentication.agent.md) — Configure Jira Cloud authentication from local secrets without exposing credentials.
  + Keywords: Jira authentication, Jira API token, secure credentials, secret manager, authorization header
  + Target: `work/module03-task/**`
- [`./test-booking-sandbox-enforcement.agent.md`](./test-booking-sandbox-enforcement.agent.md) — Test that booking execution is restricted to the configured Sandbox origin despite environment selection or edited workbook text.
  + Keywords: booking tests, Sandbox-only, environment restriction, edited workbook, safety tests, browser navigation
  + Target: `work/module03-task/**`
- [`./creating-instructions.agent.md`](./creating-instructions.agent.md) — Create and maintain portable project instructions and connect them to the workspace's agent entry points.
  + Keywords: create an instruction, update instructions, instruction catalog, Copilot setup, agent guidance
  + Target: `instructions/**`, `.github/**`, `.vscode/**`
```

## Sample Instruction
- File: instructions/add-catalog-validation.agent.md
- Contents:
```markdown
- **Input format:** Accept a path to an `.xlsx` catalog containing a `Test Cases` worksheet with the headers defined by `create_test_catalog.py`; read rows by header name, not hard-coded column positions. Use the configured Jira base URL and project key when validating issue references.
- **Input constraints:** Treat each non-empty data row as one test case; ignore wholly blank rows. Report an unreadable workbook, missing worksheet, duplicate/missing headers, or unsupported workbook structure as a catalog-level error.
- **Processing:** Validate required fields against the project schema and workbook template. Keep optional fields optional unless the schema makes them conditionally required, such as reviewer and review date for an approved case.
- **Processing:** Check that case IDs are non-empty and unique across the workbook; normalize surrounding whitespace and compare case-insensitively for duplicate detection.
- **Processing:** Validate Jira issue keys against the configured project key and issue-key format. Validate Jira links as absolute HTTPS issue URLs on the configured Jira origin, and require the link's issue key to match the row's Jira Issue Key. Do not make live Jira requests during local validation.
- **Processing:** Validate Journey, Priority, Review Status, Automation Status, and Last Result against the allowed values defined by the catalog schema; do not silently normalize invalid values into valid ones.
- **Processing:** Require Steps to contain one or more numbered actions in ascending sequence starting at `1`, with non-empty action text and no duplicate, missing, or out-of-order numbers.
- **Processing:** Collect all row-level errors rather than stopping at the first invalid case. Use Excel's 1-based row numbers, including the header row, and identify the column by its exact header.
- **Output format:** Return a validation result with an overall `valid`/`invalid` outcome, counts of checked rows and errors, and one error entry per issue containing `row`, `column`, and a concise actionable `message`. For workbook-level errors, identify the worksheet or header and leave `row` blank when no data row applies.
- **Output constraints:** Validation must be read-only and must not modify or overwrite the workbook. Use a stable, documented result shape suitable for both CLI display and automated tests; never report a valid outcome when validation failed.
- **Output constraints:** Keep errors actionable and avoid exposing credentials or unrelated row data. Add tests for valid catalogs, each validation rule, multiple errors in one run, and workbook-level failures.
```
