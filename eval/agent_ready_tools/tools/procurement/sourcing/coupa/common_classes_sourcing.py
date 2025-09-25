from enum import StrEnum
from typing import Optional

from pydantic.dataclasses import dataclass


class LinesType(StrEnum):
    """Enum specifying the lines type in Coupa."""

    ITEM = "QuoteRequestQuantityLine"
    SERVICE = "QuoteRequestAmountLine"


@dataclass
class CoupaQuoteSupplier:
    """Response in Quote Supplier."""

    id: Optional[int]
    name: Optional[str]
    email: Optional[str]


@dataclass
class CoupaCommodity:
    """Response in Commodity."""

    id: Optional[int]
    name: Optional[str]


@dataclass
class CoupaCurrency:
    """Response in Currency."""

    code: Optional[str]


@dataclass
class CoupaQuoteRequestLines:
    """Response in Quote Requests lines."""

    line_id: Optional[int]
    type: Optional[str]
    quantity: Optional[str]
    price_amount: Optional[float]
    description: Optional[str]
    need_by_date: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    price_currency: Optional[CoupaCurrency]
    commodity: Optional[CoupaCommodity]


@dataclass
class CoupaUser:
    """Response in User who create or update."""

    id: Optional[int]
    fullname: Optional[str]
    email: Optional[str]


@dataclass
class CoupaQuoteRequests:
    """Response in Quote Requests."""

    id: Optional[int]
    description: Optional[str]
    event_type: Optional[str]
    state: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    submit_time: Optional[str]
    quote_message: Optional[str]
    currency: Optional[CoupaCurrency]
    created_by: Optional[CoupaUser]
    updated_by: Optional[CoupaUser]
    quote_suppliers: Optional[list[CoupaQuoteSupplier]]
    commodity: Optional[CoupaCommodity]
    lines: Optional[list[CoupaQuoteRequestLines]]
