import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.converter import (
    convert,
    validate_amount,
    validate_currency,
    UnsupportedCurrencyError,
    InvalidAmountError,
)

SAMPLE_RATES = {
    "base": "USD",
    "rates": {
        "USD": 1.0,
        "INR": 95.24,
        "EUR": 0.85,
    },
}

class TestValidateAmount(unittest.TestCase):
    def test_valid_positive_number(self):
        self.assertEqual(validate_amount("150"), 150.0)

    def test_negative_amount_raises(self):
        with self.assertRaises(InvalidAmountError):
            validate_amount("-50")

    def test_non_numeric_amount_raises(self):
        with self.assertRaises(InvalidAmountError):
            validate_amount("abc")


class TestConvert(unittest.TestCase):
    def test_happy_path_usd_to_inr(self):
        result = convert("100", "USD", "INR", SAMPLE_RATES)
        self.assertEqual(result, 9524.0)

    def test_happy_path_inr_to_usd(self):
        result = convert("9524", "INR", "USD", SAMPLE_RATES)
        self.assertEqual(result, 100.0)

    def test_invalid_currency_raises(self):
        with self.assertRaises(UnsupportedCurrencyError):
            convert("50", "USD", "XYZ", SAMPLE_RATES)

    def test_negative_amount_raises(self):
        with self.assertRaises(InvalidAmountError):
            convert("-50", "USD", "INR", SAMPLE_RATES)


if __name__ == "__main__":
    unittest.main()

