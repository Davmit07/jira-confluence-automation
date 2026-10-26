# Python Calculator

A simple Python calculator project with a `Calculator` class for addition, subtraction, multiplication, and division.

## Multiplication

Create a `Calculator` instance and call its `multiply(first_number, second_number)` method to get the product of two numbers. For example, `Calculator().multiply(10, 4)` returns `40`.

Run the example from this directory with:

```sh
python3 main.py
```

## Vehicle Shop test-case catalog

Install the workbook dependency and generate a blank, Jira-traceable test-case catalog:

```sh
python3 -m pip install -r requirements.txt
python3 create_test_catalog.py
```

The command creates `test-cases-template.xlsx` in the current directory. Pass an
output path to choose another location, or add `--force` to replace an existing
workbook. The workbook includes the required case and Jira fields, review and
journey/priority/automation status dropdowns, reviewer and review-date fields,
and a Read Me sheet. Keep generated cases in Draft until a QA owner reviews and
approves them; workbook content is not executable.

### Populated synthetic shop catalog

Generate a separate, validated workbook with 12 draft examples: positive,
validation/empty-state, and failure/recovery coverage for Search, Compare,
Configure, and Booking:

```sh
python3 create_shop_catalog.py
```

The default output is `reports/vehicle-shop-test-catalog.xlsx`; the blank template
and existing reports are not changed. An optional output path and `--force` work
as above. Writes are staged and validated before atomic publication, and a
concurrent writer's file is not replaced without `--force`.

The examples use project `EPMCDMETST` and the Jira origin `https://jiraeu.epam.com`
(the supplied project URL is `https://jiraeu.epam.com/projects/EPMCDMETST/`).
**Issue numbers 1-4 and all scenarios are synthetic, not retrieved or verified
Jira stories or acceptance criteria.** No Jira content is fetched or sent to an AI
provider. Override the reference configuration if needed:

```sh
python3 create_shop_catalog.py reports/my-shop-catalog.xlsx \
  --jira-base-url https://jira.example --project-key SHOP
```

All rows start as **Draft / Not Mapped / Not Run**, with no reviewer, review date,
or automation ID. Named synthetic datasets and UI failure fixtures are proposals,
not implemented fixtures. QA must replace illustrative story references, confirm
acceptance criteria, define repeatable setup/reset/cleanup, and review each case.
Booking examples additionally require an application-owner-approved Sandbox and
simulated booking/payment flow; never use real customer or payment data.

### Read-only catalog validation

```sh
python3 validate_test_catalog.py reports/vehicle-shop-test-catalog.xlsx \
  --jira-base-url https://jiraeu.epam.com/projects/EPMCDMETST/ \
  --project-key EPMCDMETST
python3 -m unittest discover -s tests -p 'test_*catalog.py' -v
```

Validation is offline, never saves the workbook, and reads columns by exact
header name, so columns may be reordered. Wholly blank rows are ignored.
Headers must contain every template column exactly once. Unknown headers,
unheaded data, merged cells, formulas/error cells, non-text fields (other than
review dates), and non-`.xlsx` inputs are rejected.

Required fields are Case ID, Jira Issue Key, Jira Issue Link, Journey, Title,
Priority, Preconditions, Steps, Expected Results, Review Status, Automation
Status, and Last Result. Test Data Reference, Reviewer, Review Date, and Automation
ID are optional except that Approved rows require Reviewer and Review Date,
and Implemented rows require Automation ID. Dates must be valid Excel dates or
`YYYY-MM-DD`. Case IDs are compared after trimming surrounding whitespace and
case-folding; dropdown values must match exactly and are never repaired silently.
Steps require one non-empty numbered action per line, starting at 1 without
gaps, duplicates, or reordered numbers (`1. Action` or `1) Action`).

Jira issue keys must match the configured project and a positive issue number.
Links must be absolute HTTPS `/browse/KEY` URLs on the configured origin
(scheme, hostname, effective port), without credentials, queries, or fragments,
and match the row's issue key. A project URL may be supplied as configuration;
its path is not part of the origin. Validation checks structure only, not Jira
issue existence, QA authorization, automation registry membership, or target
environment safety.

The stable JSON result contains `outcome` (`valid` or `invalid`), `checked_rows`,
`error_count`, and `errors`. Each error has `row`, `column`, and `message`. Rows are
Excel's 1-based row numbers, including the header. Catalog-level errors use
`row: null` and name the worksheet/header in `column`; unreadable files use
`column: "Workbook"`. All row errors are collected. Structural failures return
before checking data rows. An empty template is valid with `checked_rows: 0`,
which does **not** mean there are runnable cases.

Example invalid result:

```json
{
  "outcome": "invalid",
  "checked_rows": 1,
  "error_count": 1,
  "errors": [
    {"row": 2, "column": "Title", "message": "Required field must contain text."}
  ]
}
```

CLI exit codes: `0` valid, `1` invalid catalog (including unreadable workbooks),
`2` invalid CLI arguments/configuration. The Python function
`validate_test_catalog(path, jira_base_url, project_key)` returns the same result;
invalid configuration raises `ValueError`.

This catalog workflow does not implement or enable the browser runner. A future
runner must reject unapproved/unmapped cases and use a fixed implemented
automation registry, explicit on-demand confirmation, exact-origin allowlisting,
independent production denial, and Sandbox-only booking enforcement before
navigation. Editable workbook text is never executable or a trusted safety rule.

## Offline candy-shop Sandbox example

Run a simulated purchase of one candy, without real payments, orders, or network
requests:

```sh
python3 candy_sandbox.py
python3 -m unittest discover -s tests -p 'test_candy_sandbox.py'
```

The example uses the reserved synthetic origin `https://sandbox.candy.example`
and a fake browser that only records destinations. Purchases require the Sandbox
environment and a fixed automation ID; editable titles and steps are never
executed. Invalid configuration, non-Sandbox origins, and unsafe redirects raise
an explicit error before any simulated navigation. Redirects are supplied as test
data and checked in advance, not discovered through real browser navigation.
This standalone training example does not implement the Vehicle Shop runner or
prove that an external application's browser/payment integration is safe.