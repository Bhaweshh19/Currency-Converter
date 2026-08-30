import argparse
import sys

from src.logger import setup_logger
from src.converter import (
    load_rates,
    fetch_live_rates,
    convert,
    CurrencyConverterError,
)

logger = setup_logger()


def build_parser():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Convert an amount from one currency to another.",
    )
    parser.add_argument("--from", dest="from_currency", help="Currency code to convert FROM, e.g. USD")
    parser.add_argument("--to", dest="to_currency", help="Currency code to convert TO, e.g. EUR")
    parser.add_argument("--amount", dest="amount", help="Amount to convert, e.g. 150")
    parser.add_argument(
        "--update-rates",
        action="store_true",
        help="Fetch fresh exchange rates from a live API and overwrite rates.json",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.update_rates:
        try:
            fetch_live_rates()
            print("rates.json updated successfully from the live exchange rate API.")
        except CurrencyConverterError as e:
            logger.error(str(e))
            print(f"Error: {e}")
            sys.exit(1)
        return

    if not (args.from_currency and args.to_currency and args.amount):
        parser.print_help()
        sys.exit(1)

    try:
        rates_data = load_rates()
        result = convert(args.amount, args.from_currency, args.to_currency, rates_data)
        print(f"{args.amount} {args.from_currency.upper()} = {result} {args.to_currency.upper()}")

    except CurrencyConverterError as e:
        logger.error(str(e))
        print(f"Error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print("Error: Something unexpected went wrong. Check app.log for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()

