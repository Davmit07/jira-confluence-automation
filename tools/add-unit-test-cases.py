"""Run offline environment-safety tests: python3 tools/add-unit-test-cases.py -v.

Tests the existing candy Sandbox simulation, not a live Vehicle Shop runner.
No browser or network requests are made and no files are generated.
"""

import sys
import unittest
from pathlib import Path


PROJECT_DIRECTORY = Path(__file__).resolve().parents[1] / "work" / "module03-task"
sys.path.insert(0, str(PROJECT_DIRECTORY))

from candy_sandbox import (
    APPROVED_SANDBOX_ORIGIN,
    FakeBrowser,
    PurchaseCase,
    SANDBOX_URL,
    SandboxDenied,
    buy_candy,
    origin,
)


class EnvironmentSafetyTests(unittest.TestCase):
    def assert_denied_before_navigation(self, reason, **configuration):
        browser = FakeBrowser()
        with self.assertRaisesRegex(SandboxDenied, reason):
            buy_candy(PurchaseCase(), browser, **configuration)
        self.assertEqual(browser.navigation_history, [])

    def test_origin_parsing_normalizes_hostname_and_default_https_port(self):
        for url in (
            SANDBOX_URL,
            SANDBOX_URL + ":443",
            "https://SANDBOX.CANDY.EXAMPLE/basket",
            SANDBOX_URL + "/confirmation",
        ):
            with self.subTest(url=url):
                self.assertEqual(origin(url), APPROVED_SANDBOX_ORIGIN)

    def test_origin_parsing_preserves_nondefault_port(self):
        self.assertEqual(
            origin(SANDBOX_URL + ":8443/path"),
            ("https", "sandbox.candy.example", 8443),
        )

    def test_origin_parsing_rejects_missing_or_malformed_urls(self):
        for url in (
            None, 42, "", " ", "not-a-url", "/checkout",
            "http://sandbox.candy.example", "https://",
            "https://[sandbox.candy.example", SANDBOX_URL + ":invalid",
            SANDBOX_URL + ":65536", SANDBOX_URL + ":-1",
            "https://user:password@sandbox.candy.example",
            "https://sandbox.candy.example\\checkout",
            SANDBOX_URL + "/\tcheckout", SANDBOX_URL + "/\ncheckout",
        ):
            with self.subTest(url=url):
                with self.assertRaisesRegex(SandboxDenied, "HTTPS|malformed"):
                    origin(url)

    def test_exact_origin_allowlist_accepts_canonical_sandbox_variants(self):
        for url in (SANDBOX_URL, SANDBOX_URL + "/", SANDBOX_URL + ":443",
                    "https://SANDBOX.CANDY.EXAMPLE"):
            with self.subTest(url=url):
                browser = FakeBrowser()
                result = buy_candy(PurchaseCase(), browser, sandbox_url=url)
                self.assertEqual(result.status, "simulated")
                self.assertFalse(result.payment_processed)
                self.assertEqual(browser.navigation_history, [url.rstrip("/") + "/checkout"])
                self.assertTrue(all(
                    origin(destination) == APPROVED_SANDBOX_ORIGIN
                    for destination in browser.navigation_history
                ))

    def test_exact_origin_allowlist_denies_scheme_host_and_port_changes(self):
        for url in (
            "http://sandbox.candy.example",
            "https://qa.candy.example",
            "https://sandbox.candy.example.evil.example",
            "https://evil-sandbox.candy.example",
            SANDBOX_URL + ".",
            SANDBOX_URL + ":444",
            SANDBOX_URL + ":0",
        ):
            with self.subTest(url=url):
                self.assert_denied_before_navigation(
                    "HTTPS|approved candy origin", sandbox_url=url,
                )

    def test_production_targets_are_denied_for_every_selected_environment(self):
        for environment in ("Sandbox", "Staging", "QA", "PreProd", "Production"):
            for url in ("https://shop.candy.example", "https://production.candy.example"):
                with self.subTest(environment=environment, url=url):
                    self.assert_denied_before_navigation(
                        "approved candy origin",
                        sandbox_url=url, selected_environment=environment,
                    )

    def test_missing_and_malformed_configuration_fails_closed(self):
        for url in (
            None, "", "not-a-url", "https://", SANDBOX_URL + ":bad",
            "https://user:password@sandbox.candy.example",
            SANDBOX_URL + "/?next=https://shop.candy.example",
            SANDBOX_URL + "/#checkout",
        ):
            with self.subTest(url=url):
                self.assert_denied_before_navigation(
                    "HTTPS|malformed|queries or fragments", sandbox_url=url,
                )

    def test_non_sandbox_or_missing_environment_fails_closed(self):
        for environment in (None, "", "sandbox", "Staging", "QA", "PreProd",
                            "Production", "Unknown"):
            with self.subTest(environment=environment):
                self.assert_denied_before_navigation(
                    "require the Sandbox environment", selected_environment=environment,
                )

    def test_same_origin_redirect_chain_is_allowed(self):
        redirects = (
            SANDBOX_URL + "/basket",
            "https://SANDBOX.CANDY.EXAMPLE:443/confirmation",
        )
        browser = FakeBrowser()
        result = buy_candy(PurchaseCase(), browser, redirect_urls=redirects)
        self.assertEqual(result.status, "simulated")
        self.assertFalse(result.payment_processed)
        self.assertEqual(
            browser.navigation_history, [SANDBOX_URL + "/checkout", *redirects],
        )

    def test_unsafe_redirect_anywhere_in_chain_blocks_all_navigation(self):
        for destination in (
            "https://shop.candy.example/checkout",
            "https://production.candy.example/checkout",
            "https://sandbox.candy.example.evil.example/checkout",
            "http://sandbox.candy.example/checkout",
            SANDBOX_URL + ":444/checkout",
            SANDBOX_URL + "/confirmation?next=https://shop.candy.example",
            SANDBOX_URL + "/confirmation#external",
            "/confirmation", None, "", SANDBOX_URL + ":invalid/checkout",
        ):
            for position in range(3):
                redirects = [SANDBOX_URL + "/basket", SANDBOX_URL + "/confirmation"]
                redirects.insert(position, destination)
                with self.subTest(destination=destination, position=position):
                    self.assert_denied_before_navigation(
                        "outside|HTTPS|malformed|queries or fragments",
                        redirect_urls=tuple(redirects),
                    )


if __name__ == "__main__":
    unittest.main()
