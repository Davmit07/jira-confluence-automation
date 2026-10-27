# Python Calculator

A simple Python calculator project with a `Calculator` class for addition, subtraction, multiplication, and division.

## Local PostgreSQL 15

The development database runs only on the local machine at `127.0.0.1:5432`.
Before the first start, create a local-only password file (it is ignored by Git):

```sh
mkdir -p -m 700 .local
openssl rand -hex 32 > .local/postgres_password
chmod 600 .local/postgres_password
docker compose up -d --wait
```

Verify database access with a SQL query:

```sh
docker compose exec -T database psql -U vehicle_shop -d vehicle_shop -tAc 'SELECT 1'
```

The expected query result is `1`. Stop the service with `docker compose down`;
the named development volume is preserved. To remove the development database
and its data, use `docker compose down --volumes`.

## Multiplication

Create a `Calculator` instance and call its `multiply(first_number, second_number)` method to get the product of two numbers. For example, `Calculator().multiply(10, 4)` returns `40`.

Run the example from this directory with:

```sh
python3 main.py
```

## Vehicle Shop test-case catalog

### Versioned schema and Jira-key starter rows

From the workspace root:

```sh
python3 -m pip install -r work/module03-task/requirements.txt
python3 tools/define-corepy EPMCDMETST-123 EPMCDMETST-456 \
  --output catalog-schema-v1.0.0.xlsx
```

The filename `define-corepy` is intentional; invoke it with Python 3. It accepts
one or more distinct uppercase Jira keys from one project (up to 1,000).
The default Jira host is `https://jiraeu.epam.com`; override it using
`--jira-base-url https://jira.example`. No Jira requests are made, so supplied
keys are not verified as existing issues. A project URL may also be supplied.
Output defaults to `catalog-schema-v1.0.0.xlsx` in the current directory.
Existing workbooks are protected unless `--force` is explicitly supplied.
Writes are staged before atomic publication.

The workbook includes the existing formatted `Test Cases` and `Read Me` sheets
plus a `Schema` sheet recording version **1.0.0**, all 16 exact column names,
types, required/conditional fields, allowed values, initial states, and rules.
The shared Python contract lives in `catalog_schema.py`; the existing template
generator and validator use it too. New templates record the version in
`Read Me`. Existing workbooks are not migrated or overwritten.

Each supplied key gets a stable initial `<ISSUE-KEY>-TC-001` case ID, canonical
Jira browse link, and **Draft / Not Mapped / Not Run** states. Journey, Title,
Priority, Preconditions, Steps, and Expected Results are deliberately blank;
these are incomplete authoring rows, **not valid or runnable test cases** until
QA supplies the required content. No acceptance criteria or story details are
invented. Assign another unique case ID when adding more cases for a story.

Schema maintenance: bump the major version for incompatible field/rule changes,
minor for compatible additions, and patch for documentation corrections that do
not change accepted data. Update the shared contract, validator, tests, and
documentation together; the version label alone does not migrate old workbooks
or verify compatibility. The validator continues to accept legacy unversioned
workbooks matching the current field/rule contract.

Run the schema CLI tests from `work/module03-task`:

```sh
python3 -m unittest discover -s tests -p 'test_define_catalog_schema.py' -v
```

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

### Additional environment safety unit tests

From the workspace root, run:

```sh
python3 tools/add-unit-test-cases.py -v
```

This standalone `unittest` script tests the existing offline candy Sandbox
implementation: URL parsing, exact scheme/host/port allowlisting, production
target rejection, redirect chains, and missing or malformed configuration.
Denied purchase attempts must raise `SandboxDenied` with an actionable reason
and leave the fake browser's navigation history empty. It creates no files and
makes no network requests. Run the existing `test_candy_sandbox.py` suite above
as well for the workbook-edit and automation-ID safety cases.

Production targets are rejected by the simulation's fixed Sandbox allowlist;
these tests do not prove an independent production-denial policy for a
configurable Vehicle Shop runner. That runner and its environment configuration
remain backlog work.