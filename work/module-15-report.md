# Module 15 Completion Report

## Script Metadata
- Filename: `candy_sandbox.py` (`work/module03-task/candy_sandbox.py`)
- Language: Python
- Purpose: Runs an offline candy-purchase simulation. It validates that the configured URL and any redirect destinations use the approved synthetic Sandbox origin, then records simulated navigation using a fake browser. It does not process files or make browser/network requests.

## Script Contents
```python
"""Offline candy-purchase simulation; no browser or network integration."""

from dataclasses import dataclass, field
from typing import List, Tuple
from urllib.parse import urlsplit


SANDBOX_URL = "https://sandbox.candy.example"
APPROVED_SANDBOX_ORIGIN = ("https", "sandbox.candy.example", 443)
PURCHASE_AUTOMATION_ID = "candy.purchase"


class SandboxDenied(ValueError):
    """The simulated purchase failed a Sandbox safety check."""


def origin(url: str) -> Tuple[str, str, int]:
    if not isinstance(url, str) or not url or any(char.isspace() for char in url):
        raise SandboxDenied("Target must be a non-empty HTTPS URL without whitespace.")
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError:
        raise SandboxDenied("Target URL is malformed.") from None
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or "\\" in url
    ):
        raise SandboxDenied("Target must be an HTTPS URL without embedded credentials.")
    return parsed.scheme, parsed.hostname, port if port is not None else 443


@dataclass(frozen=True)
class PurchaseCase:
    automation_id: str = PURCHASE_AUTOMATION_ID
    title: str = "Buy one candy"
    steps: str = "1. Select a candy\n2. Simulate checkout"


@dataclass
class FakeBrowser:
    navigation_history: List[str] = field(default_factory=list)

    def navigate(self, url: str) -> None:
        self.navigation_history.append(url)


@dataclass(frozen=True)
class PurchaseResult:
    status: str
    item: str
    quantity: int
    payment_processed: bool


def buy_candy(
    case: PurchaseCase,
    browser: FakeBrowser,
    selected_environment: str = "Sandbox",
    sandbox_url: str = SANDBOX_URL,
    redirect_urls: Tuple[str, ...] = (),
) -> PurchaseResult:
    """Validate all synthetic destinations before recording a simulated purchase."""
    if origin(sandbox_url) != APPROVED_SANDBOX_ORIGIN:
        raise SandboxDenied("Sandbox configuration must use the approved candy origin.")
    if selected_environment != "Sandbox":
        raise SandboxDenied("Candy purchases require the Sandbox environment.")
    if case.automation_id != PURCHASE_AUTOMATION_ID:
        raise SandboxDenied("Unknown purchase automation ID.")

    checkout_url = sandbox_url.rstrip("/") + "/checkout"
    destinations = (checkout_url,) + redirect_urls
    for url in destinations:
        if origin(url) != APPROVED_SANDBOX_ORIGIN:
            raise SandboxDenied("Purchase destination is outside the configured Sandbox origin.")
        parsed = urlsplit(url)
        if parsed.query or parsed.fragment:
            raise SandboxDenied("Simulation destinations cannot contain queries or fragments.")
    for url in destinations:
        browser.navigate(url)
    return PurchaseResult("simulated", "candy", 1, False)


if __name__ == "__main__":
    fake_browser = FakeBrowser()
    print(buy_candy(PurchaseCase(), fake_browser))
    print("Simulated navigation:", fake_browser.navigation_history)
```

## Parameters
The script has no command-line parameters. The `buy_candy` function accepts:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `case` | Purchase case; its automation ID must match the fixed purchase automation ID. | Required; `PurchaseCase()` uses `"candy.purchase"` |
| `browser` | Fake browser instance that records permitted destination URLs. | Required; `FakeBrowser()` starts with empty navigation history |
| `selected_environment` | Selected environment; purchases are permitted only in Sandbox. | `"Sandbox"` |
| `sandbox_url` | Configured base URL; must match the approved HTTPS Sandbox origin. | `SANDBOX_URL` (`https://sandbox.candy.example`) |
| `redirect_urls` | Additional destination URLs to validate before any navigation is recorded. | `()` |

## Test Run Output
Command: `python3 work/module03-task/candy_sandbox.py`

```text
PurchaseResult(status='simulated', item='candy', quantity=1, payment_processed=False)
Simulated navigation: ['https://sandbox.candy.example/checkout']
```
