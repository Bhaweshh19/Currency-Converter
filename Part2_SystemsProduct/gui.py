import tkinter as tk
from tkinter import ttk

from src.logger import setup_logger
from src.converter import load_rates, convert, CurrencyConverterError

logger = setup_logger()

# A small lookup for readable names. Not exhaustive - unlisted codes
# just show their code by themselves, which is still fine.
CURRENCY_NAMES = {
    "AED": "UAE Dirham", "AFN": "Afghan Afghani", "ALL": "Albanian Lek",
    "AMD": "Armenian Dram", "ANG": "Neth. Antillean Guilder", "AOA": "Angolan Kwanza",
    "ARS": "Argentine Peso", "AUD": "Australian Dollar", "AWG": "Aruban Florin",
    "AZN": "Azerbaijani Manat", "BAM": "Bosnia Convertible Mark", "BBD": "Barbadian Dollar",
    "BDT": "Bangladeshi Taka", "BGN": "Bulgarian Lev", "BHD": "Bahraini Dinar",
    "BIF": "Burundian Franc", "BMD": "Bermudan Dollar", "BND": "Brunei Dollar",
    "BOB": "Bolivian Boliviano", "BRL": "Brazilian Real", "BSD": "Bahamian Dollar",
    "BTN": "Bhutanese Ngultrum", "BWP": "Botswanan Pula", "BYN": "Belarusian Ruble",
    "BZD": "Belize Dollar", "CAD": "Canadian Dollar", "CDF": "Congolese Franc",
    "CHF": "Swiss Franc", "CLP": "Chilean Peso", "CNY": "Chinese Yuan",
    "COP": "Colombian Peso", "CRC": "Costa Rican Colon", "CUP": "Cuban Peso",
    "CVE": "Cape Verdean Escudo", "CZK": "Czech Koruna", "DJF": "Djiboutian Franc",
    "DKK": "Danish Krone", "DOP": "Dominican Peso", "DZD": "Algerian Dinar",
    "EGP": "Egyptian Pound", "ERN": "Eritrean Nakfa", "ETB": "Ethiopian Birr",
    "EUR": "Euro", "FJD": "Fijian Dollar", "FKP": "Falkland Islands Pound",
    "FOK": "Faroese Krona", "GBP": "British Pound", "GEL": "Georgian Lari",
    "GGP": "Guernsey Pound", "GHS": "Ghanaian Cedi", "GIP": "Gibraltar Pound",
    "GMD": "Gambian Dalasi", "GNF": "Guinean Franc", "GTQ": "Guatemalan Quetzal",
    "GYD": "Guyanaese Dollar", "HKD": "Hong Kong Dollar", "HNL": "Honduran Lempira",
    "HRK": "Croatian Kuna", "HTG": "Haitian Gourde", "HUF": "Hungarian Forint",
    "IDR": "Indonesian Rupiah", "ILS": "Israeli New Shekel", "IMP": "Isle of Man Pound",
    "INR": "Indian Rupee", "IQD": "Iraqi Dinar", "IRR": "Iranian Rial",
    "ISK": "Icelandic Krona", "JEP": "Jersey Pound", "JMD": "Jamaican Dollar",
    "JOD": "Jordanian Dinar", "JPY": "Japanese Yen", "KES": "Kenyan Shilling",
    "KGS": "Kyrgystani Som", "KHR": "Cambodian Riel", "KID": "Kiribati Dollar",
    "KMF": "Comorian Franc", "KRW": "South Korean Won", "KWD": "Kuwaiti Dinar",
    "KYD": "Cayman Islands Dollar", "KZT": "Kazakhstani Tenge", "LAK": "Laotian Kip",
    "LBP": "Lebanese Pound", "LKR": "Sri Lankan Rupee", "LRD": "Liberian Dollar",
    "LSL": "Lesotho Loti", "LYD": "Libyan Dinar", "MAD": "Moroccan Dirham",
    "MDL": "Moldovan Leu", "MGA": "Malagasy Ariary", "MKD": "Macedonian Denar",
    "MMK": "Myanmar Kyat", "MNT": "Mongolian Tugrik", "MOP": "Macanese Pataca",
    "MRU": "Mauritanian Ouguiya", "MUR": "Mauritian Rupee", "MVR": "Maldivian Rufiyaa",
    "MWK": "Malawian Kwacha", "MXN": "Mexican Peso", "MYR": "Malaysian Ringgit",
    "MZN": "Mozambican Metical", "NAD": "Namibian Dollar", "NGN": "Nigerian Naira",
    "NIO": "Nicaraguan Cordoba", "NOK": "Norwegian Krone", "NPR": "Nepalese Rupee",
    "NZD": "New Zealand Dollar", "OMR": "Omani Rial", "PAB": "Panamanian Balboa",
    "PEN": "Peruvian Sol", "PGK": "Papua New Guinean Kina", "PHP": "Philippine Peso",
    "PKR": "Pakistani Rupee", "PLN": "Polish Zloty", "PYG": "Paraguayan Guarani",
    "QAR": "Qatari Rial", "RON": "Romanian Leu", "RSD": "Serbian Dinar",
    "RUB": "Russian Ruble", "RWF": "Rwandan Franc", "SAR": "Saudi Riyal",
    "SBD": "Solomon Islands Dollar", "SCR": "Seychellois Rupee", "SDG": "Sudanese Pound",
    "SEK": "Swedish Krona", "SGD": "Singapore Dollar", "SHP": "Saint Helena Pound",
    "SLE": "Sierra Leonean Leone", "SLL": "Sierra Leonean Leone (old)", "SOS": "Somali Shilling",
    "SRD": "Surinamese Dollar", "SSP": "South Sudanese Pound", "STN": "Sao Tome & Principe Dobra",
    "SYP": "Syrian Pound", "SZL": "Swazi Lilangeni", "THB": "Thai Baht",
    "TJS": "Tajikistani Somoni", "TMT": "Turkmenistani Manat", "TND": "Tunisian Dinar",
    "TOP": "Tongan Paanga", "TRY": "Turkish Lira", "TTD": "Trinidad & Tobago Dollar",
    "TVD": "Tuvaluan Dollar", "TWD": "New Taiwan Dollar", "TZS": "Tanzanian Shilling",
    "UAH": "Ukrainian Hryvnia", "UGX": "Ugandan Shilling", "USD": "US Dollar",
    "UYU": "Uruguayan Peso", "UZS": "Uzbekistani Som", "VES": "Venezuelan Bolivar",
    "VND": "Vietnamese Dong", "VUV": "Vanuatu Vatu", "WST": "Samoan Tala",
    "XAF": "Central African CFA Franc", "XCD": "East Caribbean Dollar", "XCG": "Caribbean Guilder",
    "XDR": "Special Drawing Rights", "XOF": "West African CFA Franc", "XPF": "CFP Franc",
    "YER": "Yemeni Rial", "ZAR": "South African Rand", "ZMW": "Zambian Kwacha",
    "ZWG": "Zimbabwe Gold", "ZWL": "Zimbabwean Dollar",
}

rates_data = load_rates()
currency_codes = sorted(rates_data["rates"].keys())


def describe(code):
    name = CURRENCY_NAMES.get(code, "")
    return f"{code} - {name}" if name else code


window = tk.Tk()
window.title("Currency Converter")
window.geometry("400x260")

frame = tk.Frame(window, padx=20, pady=20)
frame.pack(fill="both", expand=True)

# --- Amount ---
tk.Label(frame, text="Amount:").grid(row=0, column=0, sticky="w", pady=8)
amount_entry = tk.Entry(frame, width=15)
amount_entry.grid(row=0, column=1, sticky="w")

# --- From currency ---
tk.Label(frame, text="From:").grid(row=1, column=0, sticky="w", pady=8)
from_var = tk.StringVar(value="USD")
from_dropdown = ttk.Combobox(frame, textvariable=from_var, values=currency_codes, width=12, state="readonly")
from_dropdown.grid(row=1, column=1, sticky="w")
from_name_label = tk.Label(frame, text=describe("USD"), fg="gray", font=("Arial", 9))
from_name_label.grid(row=1, column=2, sticky="w", padx=(10, 0))

# --- To currency ---
tk.Label(frame, text="To:").grid(row=2, column=0, sticky="w", pady=8)
to_var = tk.StringVar(value="INR")
to_dropdown = ttk.Combobox(frame, textvariable=to_var, values=currency_codes, width=12, state="readonly")
to_dropdown.grid(row=2, column=1, sticky="w")
to_name_label = tk.Label(frame, text=describe("INR"), fg="gray", font=("Arial", 9))
to_name_label.grid(row=2, column=2, sticky="w", padx=(10, 0))


def on_from_change(event):
    from_name_label.config(text=describe(from_var.get()))


def on_to_change(event):
    to_name_label.config(text=describe(to_var.get()))


from_dropdown.bind("<<ComboboxSelected>>", on_from_change)
to_dropdown.bind("<<ComboboxSelected>>", on_to_change)

# --- Result label ---
result_label = tk.Label(frame, text="", font=("Arial", 12, "bold"), fg="green")
result_label.grid(row=3, column=0, columnspan=3, pady=15)


def on_convert_click():
    result_label.config(text="", fg="green")
    try:
        result = convert(amount_entry.get(), from_var.get(), to_var.get(), rates_data)
        result_label.config(
            text=f"{amount_entry.get()} {from_var.get()} = {result} {to_var.get()}",
            fg="green",
        )
    except CurrencyConverterError as e:
        logger.error(str(e))
        result_label.config(text=str(e), fg="red")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        result_label.config(text="Something went wrong. Check app.log.", fg="red")


convert_button = tk.Button(frame, text="Convert", command=on_convert_click, width=15)
convert_button.grid(row=4, column=0, columnspan=3, pady=10)

window.mainloop()