# Run Environment Safety Test Cases

## When to Use

- Use [the unit-test script](../tools/add-unit-test-cases.py) when asked to run or extend tests for environment URL parsing, exact-origin allowlisting, production-target rejection, redirects, or missing/malformed configuration.
- Run it after changing [the offline Sandbox implementation](../work/module03-task/candy_sandbox.py) to check for safety regressions.
- The script contains and runs existing `unittest` cases. Despite its name, it does not generate test files or accept Jira keys, environment URLs, or workbook paths.
- Its scope is the offline candy-shop simulation, not a live Vehicle Shop runner. Production targets are denied by a fixed Sandbox allowlist; passing tests do not prove an independent production-denial policy for configurable environments.

## How to Run

Use Python 3 from the workspace root; no third-party packages are required:

```sh
python3 tools/add-unit-test-cases.py -v
```

To run one specific test:

```sh
python3 tools/add-unit-test-cases.py EnvironmentSafetyTests.test_unsafe_redirect_anywhere_in_chain_blocks_all_navigation -v
```

Use `python3 tools/add-unit-test-cases.py --help` for standard `unittest` options.
From another directory, use the script's absolute path; it resolves its project
imports relative to its own location.

Also run the existing Sandbox regression suite. From the workspace root:

```sh
cd work/module03-task
python3 -m unittest discover -s tests -p 'test_candy_sandbox.py' -v
```

The working directory for the second command must be `work/module03-task` so its
imports resolve. Do not run that suite from the workspace root without configuring
the import path.

## Extending Coverage

- Read the current script and implementation before editing; follow the existing `unittest.TestCase` and `subTest` patterns.
- Use synthetic reserved `.example` URLs, dummy case data, and `FakeBrowser` only. Never contact a real application, production service, or payment system.
- Check scheme, hostname, and effective port independently. Include accepted Sandbox variants and denied lookalike hosts, non-HTTPS schemes, and unapproved ports.
- Cover missing/malformed configuration and unsafe redirects at different positions in an otherwise allowed chain. Redirects are supplied and checked in advance, not discovered by a real browser.
- For denied purchases, assert both an explicit `SandboxDenied` reason and an empty navigation history. For allowed cases, assert the exact expected navigation history, simulated result, and no processed payment.
- Do not weaken assertions, silently skip failures, or modify the allowlist to make an unsafe case pass. Surface failures for investigation.

## Presenting Results

- Report the exact commands, working directories, exit codes, test totals, and any failures/errors from the actual run. Do not infer success from a prior run.
- Distinguish top-level test counts from parameterized `subTest` scenarios; do not count every scenario as a separate discovered test.
- Treat import errors, missing files, and other execution failures as failed validation, not as evidence that safety checks passed.
- Explain that all navigation is simulated and no live browser/network or payment verification occurred. Do not mark Vehicle Shop runner safety work complete solely because these simulation tests pass.
