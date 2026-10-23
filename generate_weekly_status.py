import argparse
import base64
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


PROJECT_DIR = Path(__file__).resolve().parent
JIRA_FIELDS = "summary,status,priority,assignee,duedate,resolutiondate"


def load_env_file(path):
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(key.strip(), value)


def jql_quote(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


class AtlassianClient:
    def __init__(self, base_url, email, api_token):
        self.base_url = base_url.rstrip("/")
        credentials = f"{email}:{api_token}".encode("utf-8")
        encoded_credentials = base64.b64encode(credentials).decode("ascii")
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}",
        }

    def get_json(self, path, params):
        url = f"{self.base_url}{path}?{urlencode(params)}"
        request = Request(url, headers=self.headers)
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            raise RuntimeError(
                f"Atlassian API returned HTTP {error.code} for {path}; "
                "check the token, scopes, and account access."
            ) from None
        except URLError as error:
            raise RuntimeError(f"Could not connect to Atlassian: {error.reason}") from None

    def jira_issues(self, jql):
        issues = []
        next_page_token = None

        while True:
            params = {
                "jql": jql,
                "fields": JIRA_FIELDS,
                "maxResults": "100",
            }
            if next_page_token:
                params["nextPageToken"] = next_page_token
            result = self.get_json("/rest/api/3/search/jql", params)
            issues.extend(result.get("issues", []))
            next_page_token = result.get("nextPageToken")
            if not next_page_token:
                return issues

    def updated_confluence_pages(self, space_key, since):
        cql = (
            f"space = {jql_quote(space_key)} AND type = page "
            f"AND lastmodified >= {jql_quote(since.isoformat())} "
            "ORDER BY lastmodified DESC"
        )
        result = self.get_json(
            "/wiki/rest/api/content/search",
            {"cql": cql, "limit": "50", "expand": "history.lastUpdated"},
        )
        return result.get("results", [])


def issue_line(issue):
    fields = issue.get("fields", {})
    status = (fields.get("status") or {}).get("name", "Unknown status")
    priority = (fields.get("priority") or {}).get("name", "Unprioritized")
    assignee = (fields.get("assignee") or {}).get("displayName", "Unassigned")
    summary = " ".join(fields.get("summary", "No summary").splitlines())
    attributes = [f"status: {status}", f"priority: {priority}", f"owner: {assignee}"]
    if fields.get("duedate"):
        attributes.append(f"due: {fields['duedate']}")
    return f"- {issue.get('key', 'Unknown key')}: {summary} ({'; '.join(attributes)})"


def confluence_page_line(base_url, page):
    title = " ".join(page.get("title", "Untitled page").splitlines())
    title = title.replace("[", "\\[").replace("]", "\\]")
    webui = (page.get("_links") or {}).get("webui")
    if webui:
        if webui.startswith("http://") or webui.startswith("https://"):
            page_url = webui
        elif webui.startswith("/wiki/"):
            page_url = f"{base_url}{webui}"
        else:
            page_url = f"{base_url}/wiki{webui}"
        title = f"[{title}]({page_url})"

    updated = ((page.get("history") or {}).get("lastUpdated") or {}).get("when")
    updated_label = f" (updated {updated[:10]})" if updated else ""
    return f"- {title}{updated_label}"


def section_items(items, empty_message, formatter):
    if not items:
        return [f"- {empty_message}"]
    return [formatter(item) for item in items]


def build_report(manager_name, project_key, today, completed, pages, blockers, planned, base_url):
    period_start = today - timedelta(days=6)
    next_week_start = today + timedelta(days=7 - today.weekday())
    next_week_end = next_week_start + timedelta(days=6)
    lines = [
        "# Weekly Engineering Status",
        f"- Engineering manager: {manager_name}",
        f"- Team/project: {project_key}",
        f"- Reporting week: {period_start.isoformat()} - {today.isoformat()}",
        "",
        "## Accomplishments",
        "### Jira completed",
        *section_items(completed, "No Jira issues resolved during this reporting period.", issue_line),
        "",
        "### Confluence pages updated",
        *section_items(
            pages,
            "No Confluence pages updated during this reporting period.",
            lambda page: confluence_page_line(base_url, page),
        ),
        "",
        "## Blockers",
        *section_items(blockers, "No issues found in the configured blocked statuses.", issue_line),
        "",
        f"## Next Week's Plan ({next_week_start.isoformat()} - {next_week_end.isoformat()})",
        *section_items(planned, "No incomplete Jira issues are due next week.", issue_line),
        "",
    ]
    return "\n".join(lines)


def required_setting(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing {name}; set it in the local .env file.")
    return value


def main():
    parser = argparse.ArgumentParser(description="Generate a weekly Jira and Confluence status report.")
    parser.add_argument("--output", type=Path, help="Output Markdown path (default: dated file in this folder).")
    args = parser.parse_args()

    load_env_file(PROJECT_DIR / ".env")
    try:
        base_url = required_setting("ATLASSIAN_BASE_URL").rstrip("/")
        email = required_setting("ATLASSIAN_EMAIL")
        api_token = required_setting("JIRA_TOKEN")
        project_key = required_setting("JIRA_PROJECT_KEY")
        space_key = required_setting("CONFLUENCE_SPACE_KEY")
    except RuntimeError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 2

    today = date.today()
    period_start = today - timedelta(days=6)
    next_week_start = today + timedelta(days=7 - today.weekday())
    next_week_end = next_week_start + timedelta(days=6)
    project = jql_quote(project_key)
    blocked_statuses = [
        status.strip()
        for status in os.environ.get("JIRA_BLOCKED_STATUSES", "Blocked,Impeded").split(",")
        if status.strip()
    ]
    if not blocked_statuses:
        print("Configuration error: JIRA_BLOCKED_STATUSES must contain at least one status.", file=sys.stderr)
        return 2

    client = AtlassianClient(base_url, email, api_token)
    try:
        completed = client.jira_issues(
            f"project = {project} AND statusCategory = Done "
            f"AND resolutiondate >= {jql_quote(period_start.isoformat())} "
            "ORDER BY resolutiondate DESC"
        )
        status_values = ", ".join(jql_quote(status) for status in blocked_statuses)
        blockers = client.jira_issues(
            f"project = {project} AND status in ({status_values}) "
            "AND statusCategory != Done ORDER BY priority DESC, updated DESC"
        )
        planned = client.jira_issues(
            f"project = {project} AND statusCategory != Done "
            f"AND duedate >= {jql_quote(next_week_start.isoformat())} "
            f"AND duedate <= {jql_quote(next_week_end.isoformat())} "
            "ORDER BY duedate ASC, priority DESC"
        )
        pages = client.updated_confluence_pages(space_key, period_start)
    except RuntimeError as error:
        print(f"Report generation failed: {error}", file=sys.stderr)
        return 1

    report = build_report(
        os.environ.get("MANAGER_NAME", "Engineering Manager"),
        project_key,
        today,
        completed,
        pages,
        blockers,
        planned,
        base_url,
    )
    output_path = args.output or PROJECT_DIR / f"weekly-status-{today.isoformat()}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Weekly status report written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())