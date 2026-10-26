# Core Instructions for Starting an Ecommerce Demo

## When to Use

- Use this workflow to scope, build, test, and demonstrate an ecommerce shop with synthetic products and simulated orders.
- Treat this as a demo, not a production store or authorization to take payments, fulfill orders, or collect real customer data.
- The [Define Core tool](../tools/define-core.py) only creates Jira-linked Excel authoring catalogs. Do not use it to invent shop requirements or generate an application. Use [its instructions](./use-define-core.md) only when a test-catalog workbook is separately requested with user-supplied Jira keys.

## 1. Establish the Demo Scope

- Inspect the target project and reuse its framework, conventions, and tests. If no app exists, confirm the implementation location and technology stack before scaffolding.
- Default to a small, fictional physical-goods store, a single explicitly labeled currency, guest checkout, and synthetic seed data. State these assumptions; confirm changes that affect architecture or behavior.
- Include product browsing, search/filtering, product details, cart management, simulated checkout, and order confirmation.
- Exclude real authentication, live payment gateways, shipping integrations, email delivery, analytics, and administration unless requested separately.
- Use a responsive layout with keyboard-accessible controls, meaningful labels, visible focus, and explicit loading, empty, error, and success states.

## 2. Define the Data Contract

- Product: stable ID, name, description, category, price in integer minor units, currency, stock quantity, and a local placeholder image with useful alternative text.
- Cart item: product ID and positive integer quantity. Derive names, prices, and availability from trusted seed/catalog data rather than editable display text.
- Demo order: unique ID, item/price snapshot, quantity, subtotal, simulated shipping/tax, total, and explicit `Simulated` status. Do not claim it is paid or fulfilled.
- Use clearly fictional products and contact/address fixtures. Do not request real personal information, passwords, or payment-card details.
- Document whether state is in-memory or stored locally and how to reset it. Avoid unnecessary servers or databases for a frontend-only demo; clearly describe its limitations.

## 3. Implement the Shopping Journey

- Catalog: show seeded products and prices; support search and category filtering, including no-result and reset behavior.
- Product details: show description, price, stock status, and quantity selection; prevent adding unavailable products or quantities above available stock.
- Cart: support add, update, remove, and empty-cart states. Reject non-integer, non-positive, and excessive quantities; recalculate totals after every change.
- Pricing: use integer minor units or exact decimal arithmetic, never binary floating-point money calculations. Document shipping/tax assumptions and rounding. If omitted, explicitly label shipping and tax as zero for the demo.
- Checkout: show an order summary and a persistent "Demo only - no real payment or order" notice. Use synthetic fixture data rather than collecting real customer details.
- Place order: require explicit confirmation, prevent duplicate submissions, generate a simulated order, and clear the cart only after success. Preserve the cart and show an actionable error on failure.
- Confirmation: display the simulated order ID, items, and total without implying a real charge, delivery, reservation, or external notification.

## 4. Keep the Demo Isolated

- Default to local development and simulated checkout with no external payment, booking, or fulfillment requests.
- Keep credentials, tokens, real personal data, and payment data out of source, browser storage, workbooks, screenshots, and logs.
- Treat user input as untrusted; validate it and render it as text, never executable code or unescaped HTML.
- If a backend exists, enforce price, quantity, and order validation there too. Client-side checks are not a production security boundary.
- Require explicit approval before adding external services or publishing publicly. Use only an approved non-production destination and synthetic data; do not deploy merely because implementation is complete.

## 5. Verify the Demo

- Add focused unit tests for money totals, quantity limits, stock checks, filters, and state reset.
- Test the end-to-end happy path: browse, view details, add items, edit cart, review checkout, confirm simulated order, and view confirmation.
- Test empty cart, no search results, out-of-stock items, invalid quantities, repeated submission, and a controlled order failure. Assert that a failed order preserves the cart.
- Verify keyboard navigation, form labels, visible errors, mobile layout, and the demo notice.
- Assert that checkout makes no real payment or fulfillment requests. Use mocks or local fixtures for failure scenarios.
- Run the existing focused tests and build checks. Report exact commands and actual outcomes, including failures and anything not tested.

## 6. Prepare the Demo Handoff

- Document setup, start, test, build, and reset commands using the actual implemented project.
- Provide a short walkthrough and list supported features, synthetic datasets, storage behavior, known limitations, and excluded integrations.
- Before a requested demo deployment, confirm the destination, verify the app is responsive there, and confirm simulated checkout and demo notices still work.
- Report what was built and verified without calling the demo production-ready. A real launch requires a separate scope for payment/security review, privacy obligations, authentication, inventory, tax/shipping rules, monitoring, and operational support.
