CURRENCY CONVERTER - SYSTEMS PRODUCT (Part 2)
================================================

WHAT THIS IS
------------
A command-line currency converter built as a "Programming Systems
Product": it validates input, never crashes on bad data, logs
everything it does, is covered by automated tests, and reads its
exchange rates from an external, editable config file.


REQUIREMENTS
------------
- Python 3.8 or newer
- No external packages required.


INSTALLATION
------------
1. Make sure Python 3 is installed:
       python3 --version
2. No further installation needed for normal use.


USAGE
-----
Run from inside the Part2_SystemsProduct folder:

    python3 main.py --from USD --to EUR --amount 150

More examples:

    python3 main.py --from INR --to USD --amount 5000
    python3 main.py --from eur --to inr --amount 42.50

Currency codes are case-insensitive.


CONFIGURING EXCHANGE RATES (rates.json)
----------------------------------------
Exchange rates are stored in rates.json, relative to a base currency:

    {
      "base": "USD",
      "rates": {
        "USD": 1.0,
        "INR": 95.24,
        "EUR": 0.85,
        "GBP": 0.73
      }
    }

To add a new currency, add another "CODE": rate line. No code
changes needed.


ERROR HANDLING
---------------
The app never crashes or shows a raw Python traceback. Examples:

    python3 main.py --from USD --to EUR --amount -50
    -> Error: '-50' is not a valid amount...

    python3 main.py --from USD --to XYZ --amount 100
    -> Error: 'XYZ' is not a supported currency code...

Every conversion and every error is also logged to app.log with a
timestamp.


RUNNING THE TESTS
-------------------
From the Part2_SystemsProduct folder:

    python3 -m unittest discover tests -v

Covers: happy-path conversions, negative amounts, zero amounts,
non-numeric input, and unsupported currency codes.