from enum import StrEnum
from typing import Optional

from pydantic.dataclasses import dataclass


class SAPS4HANAContractTypes(StrEnum):
    """The type of contract."""

    QUANTITY_CONTRACT_PSE = "CMK"
    VALUE_CONTRACT_PSE = "CWK"
    QUANTITY_CONTRACT = "MK"
    VALUE_CONTRACT = "WK"


@dataclass
class SAPS4HANAContractItemDetails:
    """Represents the item details of a contract in SAP S4 HANA."""

    item_number: Optional[str] = None
    item_description: Optional[str] = None
    material: Optional[str] = None
    material_group: Optional[str] = None
    net_price: Optional[str] = None
    net_price_quantity: Optional[str] = None
    target_quantity: Optional[str] = None
    price_unit: Optional[str] = None
    production_plant: Optional[str] = None
    product_type: Optional[str] = None


@dataclass
class SAPS4HANAContractPaymentDetails:
    """Represents the payment details of a contracy in SAP S4 HANA."""

    payment_terms: Optional[str] = None
    payment_in_days1: Optional[str] = None
    cash_discount_percentage1: Optional[str] = None
    payment_in_days2: Optional[str] = None
    cash_discount_percentage2: Optional[str] = None
    net_payment_days: Optional[str] = None
    target_value: Optional[str] = None
    currency: Optional[str] = None
    exchange_rate: Optional[str] = None
    exchange_rate_fixed: Optional[bool] = False
    total_net_value: Optional[str] = None
