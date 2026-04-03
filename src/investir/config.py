import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Literal

from moneyed import Currency, get_currency
from platformdirs import user_cache_dir


class ReportFormat(str, Enum):
    UK = "UK"
    PT = "PT"


@dataclass(frozen=True)
class CountryDefaults:
    """Immutable preset of fiscal rules for a given country."""
    currency: Currency
    costs_basis: Literal["fifo", "hmrc"]
    tax_year_start_month: int
    tax_year_start_day: int


class Country(str, Enum):
    UK = "UK"
    PT = "PT"

    @property
    def defaults(self) -> CountryDefaults:
        return _COUNTRY_DEFAULTS[self]


_COUNTRY_DEFAULTS: dict[Country, CountryDefaults] = {
    Country.UK: CountryDefaults(
        currency=get_currency("GBP"),
        costs_basis="hmrc",
        tax_year_start_month=4,
        tax_year_start_day=6,
    ),
    Country.PT: CountryDefaults(
        currency=get_currency("EUR"),
        costs_basis="fifo",
        tax_year_start_month=1,
        tax_year_start_day=1,
    ),
}


@dataclass
class Config:
    strict: bool = True
    offline: bool = False
    cache_dir: Path = Path(user_cache_dir()) / "investir"
    include_fx_fees: bool = True
    log_level: int = logging.INFO
    use_colour: bool = True
    currency: Currency = field(default_factory=lambda: get_currency("GBP"))
    tax_year_start_month: int = 4
    tax_year_start_day: int = 6
    costs_basis: str = "hmrc"

    def apply_country(self, country: Country) -> None:
        """Apply all fiscal defaults for the given country."""
        defaults = country.defaults
        self.currency = defaults.currency
        self.costs_basis = defaults.costs_basis
        self.tax_year_start_month = defaults.tax_year_start_month
        self.tax_year_start_day = defaults.tax_year_start_day

    @property
    def calendar_year_fiscal(self) -> bool:
        """True if the fiscal year matches the calendar year (Jan-Dec)."""
        return self.tax_year_start_month == 1 and self.tax_year_start_day == 1

    @property
    def logging_enabled(self) -> bool:
        return self.log_level != logging.CRITICAL

    def reset(self) -> None:
        Config.__init__(self)


config = Config()
