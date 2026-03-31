import logging
from collections.abc import Callable, Iterable, Mapping, Sequence
from datetime import date
from decimal import Decimal
from typing import Final

from moneyed import Money

from investir.config import config
from investir.typing import TaxYear

logger = logging.getLogger(__name__)

TAX_YEAR_START_MONTH: Final = 4
TAX_YEAR_START_DAY: Final = 6


def date_to_tax_year(d: date) -> TaxYear:
    start_month = config.tax_year_start_month
    start_day = config.tax_year_start_day

    if start_month == 1 and start_day == 1:
        # Calendar year fiscal: the tax year is simply the year itself.
        return TaxYear(d.year)

    ty_start = date(d.year, start_month, start_day)
    return TaxYear(d.year + 1) if d >= ty_start else TaxYear(d.year)


def tax_year_short_date(tax_year: TaxYear) -> str:
    if config.calendar_year_fiscal:
        return str(tax_year)
    return f"{tax_year - 1}/{(tax_year) % 100}"


def tax_year_full_date(tax_year: TaxYear) -> str:
    if config.calendar_year_fiscal:
        return f"1st January {tax_year} to 31st December {tax_year}"

    start_month = config.tax_year_start_month
    start_day = config.tax_year_start_day
    end_day = start_day - 1

    months = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]

    def ordinal(n: int) -> str:
        if 11 <= n <= 13:
            return f"{n}th"
        return f"{n}{['th', 'st', 'nd', 'rd'][n % 10] if n % 10 < 4 else 'th'}"

    start_str = f"{ordinal(start_day)} {months[start_month]} {tax_year - 1}"
    end_str = f"{ordinal(end_day)} {months[start_month]} {tax_year}"
    return f"{start_str} to {end_str}"


def multifilter(filters: Sequence[Callable] | None, iterable: Iterable) -> Iterable:
    if not filters:
        return iterable
    return filter(lambda x: all(f(x) for f in filters), iterable)


def raise_or_warn(ex: Exception) -> None:
    if config.strict:
        raise ex
    logger.warning(ex)


def read_decimal(val: str, default: Decimal = Decimal("0.0")) -> Decimal:
    return Decimal(val) if val.strip() else default


def read_base_currency(amount: str | None) -> Money | None:
    return (
        Money(amount=amount, currency=config.base_currency)
        if amount is not None and amount.strip()
        else None
    )


def read_sterling(amount: str | None) -> Money | None:
    """Read a monetary amount as GBP (used by parsers reading GBP-denominated CSVs)."""
    return (
        Money(amount=amount, currency="GBP")
        if amount is not None and amount.strip()
        else None
    )


def money(amount: Decimal | str, currency: str) -> Money:
    if currency == "GBX":
        return Money(amount=Decimal(amount) / 100, currency="GBP")
    else:
        return Money(amount=amount, currency=currency)


def base_currency_money(amount: str) -> Money:
    return Money(amount=amount, currency=config.base_currency)


def sterling(amount: str) -> Money:
    """Create a GBP Money object (used by parsers reading GBP-denominated CSVs)."""
    from moneyed import GBP

    return Money(amount=amount, currency=GBP)


def dict2str(d: Mapping[str, str]) -> str:
    return str({k: v for k, v in d.items() if v.strip()})


def boldify(text: str) -> str:
    return f"\033[1m{text}\033[0m"
