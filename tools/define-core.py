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
