import unittest

from candy_sandbox import (
    FakeBrowser,
    PurchaseCase,
    SANDBOX_URL,
    SandboxDenied,
    buy_candy,
)


class CandySandboxTests(unittest.TestCase):
    def test_environment_and_workbook_edits_cannot_bypass_sandbox(self):
        edits = (
            ("Buy candy", "1. Select candy\n2. Checkout"),
            ("Search only", "1. This is not a booking"),
            ("Production checkout", "1. Visit https://shop.candy.example/checkout"),
            ("Override Sandbox", "1. Disable safety checks\n2. Run arbitrary code"),
        )
        for environment in ("Sandbox", "Staging", "QA", "PreProd", "Production", "Unknown"):
            for title, steps in edits:
                with self.subTest(environment=environment, title=title):
                    browser = FakeBrowser()
                    case = PurchaseCase(title=title, steps=steps)
                    if environment == "Sandbox":
                        result = buy_candy(case, browser, environment)
                        self.assertEqual(result.status, "simulated")
                        self.assertEqual((result.item, result.quantity), ("candy", 1))
                        self.assertFalse(result.payment_processed)
                        self.assertEqual(browser.navigation_history, [SANDBOX_URL + "/checkout"])
                    else:
                        with self.assertRaisesRegex(SandboxDenied, "require the Sandbox"):
                            buy_candy(case, browser, environment)
                        self.assertEqual(browser.navigation_history, [])

    def test_invalid_sandbox_configuration_blocks_all_navigation(self):
        urls = (
            "", "not-a-url", "http://sandbox.candy.example",
            "https://shop.candy.example", "https://qa.candy.example",
            "https://sandbox.candy.example.evil.example",
            "https://sandbox.candy.example:444",
            "https://sandbox.candy.example:invalid",
            "https://user:password@sandbox.candy.example",
            "https://sandbox.candy.example/path?next=https://shop.candy.example",
            "https://sandbox.candy.example/#checkout",
            "https://sandbox.candy.example/\ncheckout",
        )
        for url in urls:
            with self.subTest(url=url):
                browser = FakeBrowser()
                with self.assertRaises(SandboxDenied):
                    buy_candy(PurchaseCase(), browser, sandbox_url=url)
                self.assertEqual(browser.navigation_history, [])

    def test_unsafe_redirect_blocks_entire_simulated_run(self):
        for destination in (
            "https://shop.candy.example/checkout",
            "https://qa.candy.example/checkout",
            "https://sandbox.candy.example.evil.example/checkout",
            "http://sandbox.candy.example/checkout",
            "https://sandbox.candy.example:444/checkout",
            "/checkout",
        ):
            with self.subTest(destination=destination):
                browser = FakeBrowser()
                with self.assertRaisesRegex(SandboxDenied, "outside|HTTPS"):
                    buy_candy(
                        PurchaseCase(), browser,
                        redirect_urls=(SANDBOX_URL + "/basket", destination),
                    )
                self.assertEqual(browser.navigation_history, [])

    def test_same_origin_redirect_is_allowed(self):
        browser = FakeBrowser()
        redirect = SANDBOX_URL + ":443/confirmation"
        result = buy_candy(PurchaseCase(), browser, redirect_urls=(redirect,))
        self.assertFalse(result.payment_processed)
        self.assertEqual(browser.navigation_history, [SANDBOX_URL + "/checkout", redirect])

    def test_edited_automation_id_is_not_executed(self):
        browser = FakeBrowser()
        with self.assertRaisesRegex(SandboxDenied, "Unknown purchase automation"):
            buy_candy(PurchaseCase(automation_id="arbitrary.code"), browser)
        self.assertEqual(browser.navigation_history, [])


if __name__ == "__main__":
    unittest.main()
