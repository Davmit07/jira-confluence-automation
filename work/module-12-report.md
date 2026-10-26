# Module 12 Completion Report

## Instruction File
- Filename: use-define-core.agent.md

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


## Script File
- Filename: define-core.py
- Language: Python
```python
"""Create a versioned Excel authoring catalog from Jira keys, without Jira access.

Run: python3 tools/define-corepy EPMCDMETST-123 [EPMCDMETST-456 ...]
"""

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Sequence, Union
from urllib.parse import urlsplit


PROJECT_DIRECTORY = Path(__file__).resolve().parents[1] / "work" / "module03-task"
sys.path.insert(0, str(PROJECT_DIRECTORY))

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font

from catalog_schema import (
    DEFAULTS, FIELD_RULES, HEADERS, LISTS, REQUIRED_FIELDS, SCHEMA_VERSION,
)
from create_test_catalog import MAX_CASE_ROWS, create_test_catalog
from validate_test_catalog import jira_origin


DEFAULT_JIRA_URL = "https://jiraeu.epam.com"


def define_catalog(
    issue_keys: Sequence[str],
    output: Union[str, Path],
    jira_base_url: str = DEFAULT_JIRA_URL,
    overwrite: bool = False,
) -> Path:
    """Write a schema and incomplete Draft authoring rows, never inferred stories."""
    if not issue_keys or len(issue_keys) > MAX_CASE_ROWS:
        raise ValueError(f"Supply between 1 and {MAX_CASE_ROWS} Jira issue keys.")
    for key in issue_keys:
        if not isinstance(key, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*-[1-9][0-9]*", key):
            raise ValueError("Each Jira issue key must use uppercase PROJECT-123 format with a positive issue number.")
    if len(set(issue_keys)) != len(issue_keys):
        raise ValueError("Duplicate Jira issue keys; supply each key once.")
    if len({key.rsplit("-", 1)[0] for key in issue_keys}) != 1:
        raise ValueError("Use issue keys from one project per catalog.")
    jira_origin(jira_base_url)
    parsed = urlsplit(jira_base_url)
    base_url = f"https://{parsed.netloc}"
    output = Path(output)
    if output.suffix.lower() != ".xlsx":
        raise ValueError("Output must have an .xlsx extension.")
    if output.exists() and not overwrite:
        raise FileExistsError("Output already exists; choose another path or pass --force.")
    if not output.parent.is_dir():
        raise FileNotFoundError("Output directory does not exist.")

    with tempfile.TemporaryDirectory(prefix=".catalog-schema-", dir=output.parent) as directory:
        temporary_path = Path(directory) / "catalog.xlsx"
        create_test_catalog(temporary_path)
        workbook = load_workbook(temporary_path)
        try:
            cases = workbook["Test Cases"]
            for row_number, key in enumerate(issue_keys, start=2):
                values = {
                    **DEFAULTS,
                    "Case ID": f"{key}-TC-001",
                    "Jira Issue Key": key,
                    "Jira Issue Link": f"{base_url}/browse/{key}",
                }
                for column, header in enumerate(HEADERS, start=1):
                    cases.cell(row=row_number, column=column, value=values.get(header))
            schema = workbook.create_sheet("Schema")
            schema.append(["Schema Version", SCHEMA_VERSION])
            schema.append(["Column", "Type", "Required", "Allowed Values", "Initial Value", "Rules"])
            for header in HEADERS:
                required = "Yes" if header in REQUIRED_FIELDS else "No"
                if header in ("Reviewer", "Review Date"):
                    required = "When Approved"
                elif header == "Automation ID":
                    required = "When Implemented"
                schema.append([
                    header, "date / YYYY-MM-DD" if header == "Review Date" else "text",
                    required, ", ".join(LISTS.get(header, [])),
                    DEFAULTS.get(header), FIELD_RULES[header],
                ])
            for column, width in zip("ABCDEF", (24, 24, 24, 55, 24, 100)):
                schema.column_dimensions[column].width = width
            for row in schema:
                for cell in row:
                    cell.alignment = Alignment(vertical="top", wrap_text=True)
                    if cell.row <= 2:
                        cell.font = Font(bold=True)
            schema.freeze_panes = "A3"
            schema.auto_filter.ref = f"A2:F{len(HEADERS) + 2}"
            workbook["Read Me"].append((
                "Incomplete authoring rows",
                "Issue keys are user-supplied, not verified with Jira. Fill Journey, Title, "
                "Priority, Preconditions, Steps, and Expected Results before validation "
                "can pass. No story details or acceptance criteria have been inferred. "
                "Draft / Not Mapped rows are not runnable.",
            ))
            workbook.properties.title = f"Vehicle Shop Catalog Schema {SCHEMA_VERSION}"
            workbook.save(temporary_path)
        finally:
            workbook.close()
        if overwrite:
            os.replace(temporary_path, output)
        else:
            os.link(temporary_path, output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Define Excel catalog schema v" + SCHEMA_VERSION
        + " with incomplete Draft rows for Jira keys; no network requests.",
    )
    parser.add_argument("issue_keys", nargs="+", help="one or more keys from one project, e.g. EPMCDMETST-123")
    parser.add_argument("--jira-base-url", default=DEFAULT_JIRA_URL)
    parser.add_argument("--output", type=Path, default=Path(f"catalog-schema-v{SCHEMA_VERSION}.xlsx"))
    parser.add_argument("--force", action="store_true", help="explicitly replace an existing workbook")
    arguments = parser.parse_args()
    try:
        output = define_catalog(
            arguments.issue_keys, arguments.output, arguments.jira_base_url, arguments.force
        )
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(f"Created catalog schema v{SCHEMA_VERSION}: {output}")
    print(f"Draft authoring rows: {len(arguments.issue_keys)}; required story fields remain incomplete.")


if __name__ == "__main__":
    main()
```


## Script Execution Output
```text
usage: define-core.py [-h] [--jira-base-url JIRA_BASE_URL] [--output OUTPUT]
                      [--force]
                      issue_keys [issue_keys ...]

Define Excel catalog schema v1.0.0 with incomplete Draft rows for Jira keys;
no network requests.

positional arguments:
  issue_keys            one or more keys from one project, e.g. EPMCDMETST-123

optional arguments:
  -h, --help            show this help message and exit
  --jira-base-url JIRA_BASE_URL
  --output OUTPUT
  --force               explicitly replace an existing workbook
```
