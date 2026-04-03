from datetime import datetime, timezone
from typing import Final

from investir.config import config

# Minimum timestamp for an order. Different rules apply on orders made
# before 6 April 2008. See:
# https://www.gov.uk/hmrc-internal-manuals/capital-gains-manual/cg51570
MIN_TIMESTAMP: Final = datetime(2008, 4, 6, tzinfo=timezone.utc)

CURRENCY_CODES: Final = frozenset(
    [
        "GBP",  # Pound sterling
        "USD",  # United States dollar
        "EUR",  # Euro
        "CHF",  # Swiss franc
        "DKK",  # Danish Krone
        "NOK",  # Norwegian Krone
        "PLN",  # Polish złoty
        "SEK",  # Swedish Krona
        "CZK",  # Czech Koruna
        "RON",  # Romanian Leu
        "BGN",  # Bulgarian Lev
        "HUF",  # Hungarian Forint
    ]
)

CURRENCY_SYMBOLS: Final = {
    "GBP": "£",
    "EUR": "€",
    "USD": "$",
    "CHF": "CHF",
}


def get_base_currency():
    """Return the configured base currency."""
    return config.currency


def get_currency_symbol() -> str:
    """Return the symbol for the configured base currency."""
    return CURRENCY_SYMBOLS.get(config.currency.code, config.currency.code)
