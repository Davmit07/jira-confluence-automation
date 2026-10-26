# Calculate Compound Interest

- Use this workflow when asked to calculate compound interest, a final investment balance, or interest earned with a fixed annual rate and compounding frequency. Use [the Python tool](../tools/compound_interest.py) rather than estimating the result.
- The tool assumes no additional deposits or withdrawals and no fees or taxes. It does not calculate simple interest, variable-rate investments, or continuous compounding.
- Obtain the principal, annual percentage rate, compounds per year, and total years. Ask for missing or ambiguous inputs rather than inventing them.
- Principal, annual rate, and total years must be finite, non-negative numbers. Compounds per year must be a positive integer: use `1` for annually, `4` for quarterly, or `12` for monthly.
- Enter the annual rate as a percentage: `7.34` means 7.34%, not `0.0734`. Pass plain numeric arguments without currency symbols, thousands separators, or `%`.
- Convert years and months to decimal years using `years + months / 12`. Preserve enough precision to avoid changing the rounded result; for example, 8 years and 7 months is approximately `8.5833333333333333333333333333333333333333333333333`. Do not pass a fraction such as `103/12`, because the CLI accepts decimal numbers, not expressions.

## Invocation

Run from the workspace root with Python 3; the tool uses only the standard library:

```sh
python3 tools/compound_interest.py PRINCIPAL ANNUAL_RATE COMPOUNDS_PER_YEAR TOTAL_YEARS
```

The four arguments are positional and must appear in that order. For example:

```sh
python3 tools/compound_interest.py 1000 5 12 2
```

Expected output:

```text
Final amount: $1,104.94
Interest earned: $104.94
```

- Use `python3 tools/compound_interest.py --help` for argument help. From another directory, use the script's absolute path.
- If execution fails, report the actionable error and correct the inputs before retrying. Never present an unsuccessful run as a calculated result. Invalid inputs or unsupported numeric ranges produce an error and exit code `2`.

## Presenting Results

- State the principal, annual percentage rate, compounding frequency, and duration used, including any conversion from months to years.
- Report **Final amount** and **Interest earned** using the tool's output, with thousands separators and two decimal places. The tool uses decimal arithmetic and rounds half up to cents only at the end.
- The CLI labels amounts with `$`. Do not silently reinterpret another currency as dollars; if the user specifies another currency, label the numeric results consistently with that currency and explain that no currency conversion is performed.
- If the user requests the calculation, show `A = P * (1 + r / n) ** (n * t)` and `interest = A - P`, where `r` is the annual percentage divided by 100. Use the actual inputs and do not replace the tool's result with a hand-calculated estimate.
- Note the assumptions of a fixed rate, no additional deposits or withdrawals, and no fees or taxes when relevant. Do not imply that the result guarantees investment returns.
