"""Vehicle Shop catalog schema; bump the version when this contract changes."""

SCHEMA_VERSION = "1.0.0"
HEADERS = [
    "Case ID", "Jira Issue Key", "Jira Issue Link", "Journey", "Title", "Priority",
    "Preconditions", "Steps", "Expected Results", "Test Data Reference",
    "Review Status", "Reviewer", "Review Date", "Automation Status",
    "Automation ID", "Last Result",
]
LISTS = {
    "Journey": ["Search", "Compare", "Configure", "Booking"],
    "Priority": ["Critical", "High", "Medium", "Low"],
    "Review Status": ["Draft", "Needs Update", "Approved", "Rejected"],
    "Automation Status": ["Not Mapped", "Planned", "Implemented", "Retired"],
    "Last Result": ["Not Run", "Passed", "Failed", "Skipped"],
}
REQUIRED_FIELDS = (
    "Case ID", "Jira Issue Key", "Jira Issue Link", "Journey", "Title",
    "Priority", "Preconditions", "Steps", "Expected Results",
    "Review Status", "Automation Status", "Last Result",
)
DEFAULTS = {
    "Review Status": "Draft",
    "Automation Status": "Not Mapped",
    "Last Result": "Not Run",
}
FIELD_RULES = {
    "Case ID": "Stable unique text ID; compare trimmed values case-insensitively.",
    "Jira Issue Key": "Configured project key followed by a hyphen and positive issue number.",
    "Jira Issue Link": "HTTPS /browse/KEY URL on configured Jira origin, matching the issue key; no credentials, query, or fragment.",
    "Journey": "Choose an exact allowed value; booking execution requires approved Sandbox.",
    "Title": "Non-empty scenario title.",
    "Priority": "Choose an exact allowed value.",
    "Preconditions": "Non-empty setup, environment, and repeatability requirements.",
    "Steps": "One non-empty numbered action per line, starting at 1 with no gaps, duplicates, or reordering.",
    "Expected Results": "Non-empty observable outcomes.",
    "Test Data Reference": "Optional safe named data reference; never credentials or real customer/payment data.",
    "Review Status": "Choose an exact allowed value; new cases are Draft.",
    "Reviewer": "Required when Review Status is Approved.",
    "Review Date": "Excel date or valid YYYY-MM-DD; required when Review Status is Approved.",
    "Automation Status": "Choose an exact allowed value; new cases are Not Mapped.",
    "Automation ID": "Required when Automation Status is Implemented; runner must resolve a fixed implemented registry entry.",
    "Last Result": "Choose an exact allowed value; new cases are Not Run.",
}
