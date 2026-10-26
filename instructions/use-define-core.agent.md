# Use the Catalog Schema Tool

## When to Use

- Use [define-core.py](../tools/define-core.py) to create a versioned Vehicle Shop Excel catalog schema and initial authoring rows for supplied Jira issue keys.
- Use it when starting a catalog for QA authoring, not when retrieving Jira stories, generating acceptance criteria, running browser tests, or modifying an existing populated catalog.
- The tool works offline. It neither verifies Jira issue existence nor fetches story content, requires credentials, or sends data to an AI provider.

## Inputs and Prerequisites

- Use Python 3 with the project's `openpyxl` dependency available. If it is missing, install the declared requirements into an appropriate virtual environment:

  ```sh
  python3 -m pip install -r work/module03-task/requirements.txt
  ```

- Accept between 1 and 1,000 distinct Jira keys from a single project. Keys must use uppercase project identifiers and positive issue numbers, such as `EPMCDMETST-123`. Reject duplicates, mixed projects, malformed keys, and zero or leading-zero issue numbers.
- Obtain the keys from the user; do not invent real issue references.
- Use the default Jira host `https://jiraeu.epam.com` unless another approved HTTPS base URL is supplied. A project URL is also accepted; links are built from its origin. Embedded credentials, queries, and fragments are rejected.
- Choose an `.xlsx` output path with an existing parent directory. Never supply `--force` unless the user explicitly permits replacing that file.

## Invocation

Run from the workspace root:

```sh
python3 tools/define-core.py EPMCDMETST-123 EPMCDMETST-456 \
  --output catalog-schema-v1.0.0.xlsx
```

Available arguments:

| Argument | Meaning |
|---|---|
| `issue_keys` | Required positional keys; one or more from the same project. |
| `--jira-base-url URL` | Override the default Jira HTTPS host or supply a project URL. |
| `--output PATH` | Destination workbook; defaults to `catalog-schema-v<SCHEMA_VERSION>.xlsx` in the current directory. |
| `--force` | Explicitly replace an existing destination workbook. |
| `--help` | Display CLI usage without creating a workbook. |

For another Jira host:

```sh
python3 tools/define-core.py SHOP-123 \
  --jira-base-url https://jira.example \
  --output shop-catalog.xlsx
```

From another directory, use the script's absolute path; it resolves project
imports relative to its own location. Relative output paths still resolve from
the working directory. Writes are staged before atomic publication; without
`--force`, a concurrently created destination is not overwritten.

## Output and Follow-up

- The workbook contains `Test Cases`, `Read Me`, and `Schema` worksheets. The schema sheet records the shared contract's version, all 16 columns, types, required/conditional fields, allowed values, defaults, and rules.
- Read the current version from [catalog_schema.py](../work/module03-task/catalog_schema.py); do not infer it from an output filename. The initial version is `1.0.0`. Creating a workbook does not increment the schema version or migrate existing catalogs.
- Each supplied key gets a `<ISSUE-KEY>-TC-001` case ID, matching HTTPS Jira browse link, and **Draft / Not Mapped / Not Run** states. Reviewer, review date, and automation ID remain blank.
- Journey, Title, Priority, Preconditions, Steps, and Expected Results intentionally remain blank. Clearly describe the result as an **incomplete authoring catalog**, not a valid test suite or executable automation.
- QA must fill the missing fields using verified requirements, review the cases, and assign unique IDs for additional cases. Only approved cases mapped to implemented registry entries may eventually run; workbook text must never be executed.
- After authoring, use [catalog validation](./add-catalog-validation.agent.md). For example, from the workspace root:

  ```sh
  python3 work/module03-task/validate_test_catalog.py catalog-schema-v1.0.0.xlsx \
    --jira-base-url https://jiraeu.epam.com \
    --project-key EPMCDMETST
  ```

  Untouched starter rows are expected to fail required-field validation. Catalog validity alone does not imply QA approval or automation readiness.

## Reporting and Errors

- Report the actual output path, recorded schema version, and number of Draft authoring rows after a successful run.
- State that Jira references are user-supplied and unverified, and identify the fields requiring authoring.
- Invalid inputs and file-write errors are surfaced by the CLI with exit code `2`. Report the actionable error; do not claim creation succeeded or silently choose another destination.
- Keep credentials, tokens, and real customer/payment data out of arguments, workbooks, and reports.
