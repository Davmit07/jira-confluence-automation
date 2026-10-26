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
