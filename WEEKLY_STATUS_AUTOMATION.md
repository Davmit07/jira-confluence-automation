# Weekly Status Automation

This on-demand script reads Jira and Confluence Cloud data and writes a dated Markdown report in this folder.

## Configure

1. Set the variables from `.env.example` in the ignored local `.env` file.
2. Use a newly rotated Atlassian API token. Do not commit `.env` or share the token.
3. Set the Jira project key and Confluence space key. Adjust `JIRA_BLOCKED_STATUSES` to match the project's workflow.

## Generate

Run from this folder:

```sh
python3 generate_weekly_status.py
```

The report covers Jira issues resolved in the last seven days, Jira issues in the configured blocked statuses, Jira issues due next week, and Confluence pages updated in the last seven days. To choose another output path, add `--output path/to/report.md`.

The script uses Python's standard library and Jira/Confluence REST APIs. The API token must have access to the selected project and space.