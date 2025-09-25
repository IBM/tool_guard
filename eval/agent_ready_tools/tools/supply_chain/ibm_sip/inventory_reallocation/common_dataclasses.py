from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class SIPInventoryItemSupply:
    """Represents an item supply."""

    item_id: str
    item_type: str
    unit_of_measure: str
    quantity: float
    ship_node: str
    segment: Optional[str] = None
    segment_type: Optional[str] = None
    eta: Optional[str] = None
    ship_by_date: Optional[str] = None
