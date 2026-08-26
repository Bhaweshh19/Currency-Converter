import json
import os
import logging

logger = logging.getLogger("currency_converter")

RATES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "rates.json")


# --- Custom exceptions ---
class CurrencyConverterError(Exception):
    """Base class for every error this app raises on purpose."""


class UnsupportedCurrencyError(CurrencyConverterError):
    def __init__(self, code):
        self.code = code
        super().__init__(
            f"'{code}' is not a supported currency code. "
            f"Check rates.json for the list of supported codes."
        )


class InvalidAmountError(CurrencyConverterError):
    def __init__(self, amount):
        self.amount = amount
        super().__init__(
            f"'{amount}' is not a valid amount. "
            f"Please enter a positive number, e.g. 150 or 99.99."
        )


class RatesFileError(CurrencyConverterError):
    def __init__(self, message):
        super().__init__(message)


def load_rates(filepath=RATES_FILE):
    """
    Load exchange rates from a JSON config file.
    All rates are relative to the 'base' currency.
    """
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Rates file not found at {filepath}")
        raise RatesFileError(f"Could not find rates file at: {filepath}")
    except json.JSONDecodeError as e:
        logger.error(f"Rates file is not valid JSON: {e}")
        raise RatesFileError(f"rates.json is corrupted or invalid: {e}")

    if "base" not in data or "rates" not in data:
        raise RatesFileError("rates.json must contain a 'base' key and a 'rates' key")

    return data


def validate_amount(amount_value):
    """
    Turn user input (string or number) into a positive float.
    Raises InvalidAmountError for non-numeric, zero, or negative values.
    """
    try:
        amount = float(amount_value)
    except (TypeError, ValueError):
        raise InvalidAmountError(amount_value)

    if amount <= 0:
        raise InvalidAmountError(amount_value)

    return amount


def validate_currency(code, rates_dict):
    """
    Normalise a currency code (e.g. 'usd' -> 'USD') and confirm it
    exists in the loaded rates. Raises UnsupportedCurrencyError otherwise.
    """
    if not isinstance(code, str):
        raise UnsupportedCurrencyError(code)

    normalised = code.upper().strip()
    if normalised not in rates_dict:
        raise UnsupportedCurrencyError(code)

    return normalised


def convert(amount, from_currency, to_currency, rates_data):
    """
    Convert `amount` from `from_currency` to `to_currency` using
    rates_data (already loaded from rates.json).
    """
    rates = rates_data["rates"]

    from_code = validate_currency(from_currency, rates)
    to_code = validate_currency(to_currency, rates)
    clean_amount = validate_amount(amount)

    amount_in_base = clean_amount / rates[from_code]
    converted = amount_in_base * rates[to_code]
    converted = round(converted, 2)

    logger.info(
        f"Converted {clean_amount} {from_code} -> {converted} {to_code} "
        f"(base currency: {rates_data['base']})"
    )
    return converted