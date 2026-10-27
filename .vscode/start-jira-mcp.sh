#!/bin/sh
# Starts the read-only Jira MCP server using the local, gitignored .env file.
# Credentials stay in that file and are never written to committed configuration.
set -eu

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/work/module03-task/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing work/module03-task/.env. Copy .env.example and set ATLASSIAN_BASE_URL and JIRA_TOKEN locally." >&2
  exit 1
fi

read_env() {
  awk -F= -v key="$1" '
    $0 ~ /^[[:space:]]*#/ { next }
    {
      name = $1
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", name)
      if (name == key) {
        sub(/^[^=]*=/, "")
        gsub(/\r$/, "")
        gsub(/^[[:space:]]+|[[:space:]]+$/, "")
        quote = substr($0, 1, 1)
        if (length($0) >= 2 && (quote == "\"" || quote == sprintf("%c", 39)) && substr($0, length($0), 1) == quote) {
          $0 = substr($0, 2, length($0) - 2)
        }
        print
        exit
      }
    }
  ' "$ENV_FILE"
}

JIRA_URL="$(read_env JIRA_URL)"
if [ -z "$JIRA_URL" ]; then
  JIRA_URL="$(read_env ATLASSIAN_BASE_URL)"
fi
JIRA_PERSONAL_TOKEN="$(read_env JIRA_PERSONAL_TOKEN)"
if [ -z "$JIRA_PERSONAL_TOKEN" ]; then
  JIRA_PERSONAL_TOKEN="$(read_env JIRA_TOKEN)"
fi

JIRA_URL="${JIRA_URL%/}"

case "$JIRA_URL" in
  https://*)
    ;;
  *)
    echo "Jira base URL must be an absolute HTTPS URL with a hostname." >&2
    exit 1
    ;;
esac

case "$JIRA_URL" in
  *://*@*|*\?*|*\#*)
    echo "Jira base URL must not include credentials, a query, or a fragment." >&2
    exit 1
    ;;
esac

case "$JIRA_URL" in
  https:///*|https://)
    echo "Jira base URL must include a hostname." >&2
    exit 1
    ;;
esac

if [ -z "$JIRA_PERSONAL_TOKEN" ]; then
  echo "Missing Jira personal access token. Set JIRA_TOKEN in the local .env file." >&2
  exit 1
fi

export JIRA_URL
export JIRA_PERSONAL_TOKEN
export READ_ONLY_MODE="${READ_ONLY_MODE:-true}"
unset JIRA_USERNAME JIRA_API_TOKEN JIRA_EMAIL || true

exec uvx mcp-atlassian
