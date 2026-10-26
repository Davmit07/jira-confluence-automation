"""Calculate compound interest without additional deposits or withdrawals.

Usage: python3 tools/compound_interest.py PRINCIPAL ANNUAL_RATE COMPOUNDS_PER_YEAR TOTAL_YEARS
Enter the annual rate as a percentage (7.34 means 7.34%) and years as a decimal.
"""

import argparse
from decimal import Decimal, DecimalException, ROUND_HALF_UP, localcontext
from typing import Tuple


def nonnegative_decimal(value: str) -> Decimal:
    try:
        number = Decimal(value)
    except DecimalException:
        raise argparse.ArgumentTypeError("must be a finite, non-negative number") from None
    if not number.is_finite() or number < 0:
        raise argparse.ArgumentTypeError("must be a finite, non-negative number")
    return number


def positive_integer(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("must be a positive integer") from None
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def calculate_compound_interest(
    principal: Decimal,
    annual_rate: Decimal,
    compounds_per_year: int,
    total_years: Decimal,
) -> Tuple[Decimal, Decimal]:
    """Return the final amount and interest, rounded half up to cents."""
    if any(not value.is_finite() or value < 0 for value in (
        principal, annual_rate, total_years
    )):
        raise ValueError("Principal, annual rate, and total years must be finite and non-negative.")
    if isinstance(compounds_per_year, bool) or not isinstance(compounds_per_year, int) or compounds_per_year <= 0:
        raise ValueError("Compounds per year must be a positive integer.")
    with localcontext() as context:
        context.prec = 50
        if principal == 0 or annual_rate == 0 or total_years == 0:
            amount = principal
        else:
            rate = annual_rate / Decimal(100)
            amount = principal * (
                1 + rate / compounds_per_year
            ) ** (compounds_per_year * total_years)
        cents = Decimal("0.01")
        return (
            amount.quantize(cents, rounding=ROUND_HALF_UP),
            (amount - principal).quantize(cents, rounding=ROUND_HALF_UP),
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calculate compound interest; amounts are rounded to cents.",
        epilog="Example: python3 tools/compound_interest.py 1000 5 12 2",
    )
    parser.add_argument("principal", type=nonnegative_decimal, help="initial amount")
    parser.add_argument("annual_rate", type=nonnegative_decimal, help="annual percentage rate, e.g. 7.34")
    parser.add_argument("compounds_per_year", type=positive_integer, help="e.g. 12 for monthly")
    parser.add_argument("total_years", type=nonnegative_decimal, help="duration in years; fractional years are supported")
    arguments = parser.parse_args()
    try:
        amount, interest = calculate_compound_interest(
            arguments.principal, arguments.annual_rate,
            arguments.compounds_per_year, arguments.total_years,
        )
    except DecimalException:
        parser.error("Inputs exceed the supported numeric range; use smaller values.")
    print(f"Final amount: ${amount:,.2f}")
    print(f"Interest earned: ${interest:,.2f}")


if __name__ == "__main__":
    main()
