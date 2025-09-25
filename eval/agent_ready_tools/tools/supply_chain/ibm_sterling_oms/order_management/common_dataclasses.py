from enum import Enum
from typing import Optional

from pydantic.dataclasses import dataclass


class OrderDocumentType(str, Enum):
    """The order document types."""

    SALES_ORDER = "0001"
    RETURN_ORDER = "0003"

    @classmethod
    def validate_document_type(cls, val: Optional[str]) -> Optional[str]:
        """
        Utility function to validate document types for the Enum, can be SALES_ORDER, RETURN_ORDER,
        0001, 0003, etc.

        Args:
            val: Document type value

        Returns:
            Proper value defined in the enum.
        """

        # if its None it's also fine
        if val is None:
            return None
        # can use SALES_ORDER
        if val in cls.__members__:
            return cls[val]
        try:  # can use 0001
            return cls(val)
        except ValueError:
            raise ValueError(
                f"Invalid order_type {val}. "
                f"Allowed: {list(cls.__members__.keys())} or {[e.value for e in cls]}"
            )


@dataclass
class OMSOrderHeader:
    """Represents an order."""

    order_id: str
    order_number: Optional[str]
    order_date: Optional[str]
    order_type: Optional[str]
    ship_to_id: Optional[str]
    order_status: Optional[str]
    total_amount: Optional[str]
    payment_status: Optional[str]
