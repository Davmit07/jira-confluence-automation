# Python Calculator

A simple Python calculator project with a `Calculator` class for addition, subtraction, multiplication, and division.

## Multiplication

Create a `Calculator` instance and call its `multiply(first_number, second_number)` method to get the product of two numbers. For example, `Calculator().multiply(10, 4)` returns `40`.

Run the example from this directory with:

```sh
python3 main.py
```

## Vehicle Shop test-case catalog

Install the workbook dependency and generate a blank, Jira-traceable test-case catalog:

```sh
python3 -m pip install -r requirements.txt
python3 create_test_catalog.py
```

The command creates `test-cases-template.xlsx` in the current directory. Pass an
output path to choose another location, or add `--force` to replace an existing
workbook. The workbook includes the required case and Jira fields, review and
journey/priority/automation status dropdowns, reviewer and review-date fields,
and a Read Me sheet. Keep generated cases in Draft until a QA owner reviews and
approves them; workbook content is not executable.

## Offline candy-shop Sandbox example

Run a simulated purchase of one candy, without real payments, orders, or network
requests:

```sh
python3 candy_sandbox.py
python3 -m unittest discover -s tests -p 'test_candy_sandbox.py'
```

The example uses the reserved synthetic origin `https://sandbox.candy.example`
and a fake browser that only records destinations. Purchases require the Sandbox
environment and a fixed automation ID; editable titles and steps are never
executed. Invalid configuration, non-Sandbox origins, and unsafe redirects raise
an explicit error before any simulated navigation. Redirects are supplied as test
data and checked in advance, not discovered through real browser navigation.
This standalone training example does not implement the Vehicle Shop runner or
prove that an external application's browser/payment integration is safe.