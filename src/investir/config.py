import logging
from dataclasses import dataclass, field
from pathlib import Path

from moneyed import Currency, get_currency
from platformdirs import user_cache_dir


@dataclass
class Config:
    strict: bool = True
    offline: bool = False
    cache_dir: Path = Path(user_cache_dir()) / "investir"
    include_fx_fees: bool = True
    log_level: int = logging.INFO
    use_colour: bool = True
    base_currency: Currency = field(default_factory=lambda: get_currency("GBP"))
    tax_year_start_month: int = 4
    tax_year_start_day: int = 6

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
