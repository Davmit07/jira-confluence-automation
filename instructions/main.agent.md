# Instructions Catalog

Load the relevant instruction completely before acting. Use the keywords and targets below to route requests.

- [`./start-ecommerce-demo.agent.md`](./start-ecommerce-demo.agent.md) — Define, build, test, and demonstrate an ecommerce shop using synthetic data and simulated checkout.
  + Keywords: ecommerce demo, start a shop, core shop instructions, shopping cart, simulated checkout, demo launch
- [`./use-define-core.md`](./use-define-core.md) — Create a versioned Excel catalog schema and incomplete Draft authoring rows from Jira issue keys.
  + Keywords: define core, catalog schema, schema version, Jira keys, starter catalog
  + Target: `tools/define-core.py`
- [`./use-add-test-caes.agent.md`](./use-add-test-caes.agent.md) — Run and extend offline environment safety unit tests with the existing Python script.
  + Keywords: unit test cases, URL parsing, exact-origin allowlisting, production blocking, redirects, malformed configuration
  + Target: `tools/add-unit-test-cases.py`
- [`./calculate-compound-interest.agent.md`](./calculate-compound-interest.agent.md) — Calculate compound interest with the Python CLI and present the final amount and interest earned.
  + Keywords: compound interest, investment balance, interest earned, annual rate, monthly compounding
  + Target: `tools/compound_interest.py`
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
