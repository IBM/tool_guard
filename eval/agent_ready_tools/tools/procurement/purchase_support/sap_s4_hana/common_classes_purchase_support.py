from enum import StrEnum
from typing import Optional

from pydantic.dataclasses import dataclass


class SAPS4HANAItemTextTypes(StrEnum):
    """The item text types of a purchase requisition in SAP S4 HANA."""

    ITEM_TEXT = "B01"
    ITEM_NOTE = "B02"
    DELIVERY_TEXT = "B03"
    MATERIAL_PO_TEXT = "B04"
    IN_RR_SALE_ORDER_3RD_PARTY = "B92"


class SAPS4HANAPurchaseOrderItemTextTypes(StrEnum):
    """Enum specifying the item text types of a purchase order in SAP S4 HANA."""

    ITEM_TEXT = "F01"
    INFO_RECORD_PO_TEXT = "F02"
    MATERIAL_PO_TEXT = "F03"
    DELIVERY_TEXT = "F04"
    INFO_RECORD_NOTE = "F05"
    MRP_TEXT = "F06"
    ITEM_TET_FOR_SPEC2000 = "F10"


class SAPS4HANAPurchaseOrderHeaderTextTypes(StrEnum):
    """Enum specifying the header text types of a purchase order in SAP S4 HANA."""

    TEXT = "F01"
    NOTE = "F02"
    PRICING_TYPES = "F03"
    DEADLINES = "F04"
    TERMS_OF_DELIVERY = "F05"
    SHIPPING_INSTRUCTION = "F06"
    TERMS_OF_PAYMENT = "F07"
    WARRANTIES = "F08"
    PENALTY_FOR_BREACH_OF_CONTRACT = "F09"
    GAURANTEES = "F10"
    CONTRACT_RIDERS_CLAUSES = "F11"
    ASSET = "F12"
    OTHER_CONTRACTUAL_STIPULATIONS = "F13"
    INBOUND_DELIVERY = "F14"
    VENDOR_MEMO_GENERAL = "F15"
    VENDOR_MEMO_SPECIAL = "F16"
    CUP = "F17"
    CIG = "F18"
    MGO = "F19"
    NOC = "F99"


class SAPS4HANAAccountAssignmentCategory(StrEnum):
    """The assignment category of the purchase requisition in SAP S4 HANA."""

    UNKNOWN = "U"
    ORDER = "F"
    COST_CENTRE = "K"
    SALES_ORDER = "C"
    PROJECT = "P"


class S4HANAInternationalCommercialTermsTypes(StrEnum):
    """The international commercial terms agreed upon between buyer and seller in SAP S4 HANA."""

    COSTS_AND_FREIGHT = "CFR"
    COSTS_INSURANCE_AND_FREIGHT = "CIF"
    CARRIAGE_AND_INSURANCE_PAID_TO = "CIP"
    CARRIAGE_PAID_TO = "CPT"
    DELIVERED_AT_FRONTIER = "DAF"
    DELIVERED_AT_PLACE = "DAP"
    DELIVERED_AT_TERMINAL = "DAT"
    DELIVERED_DUTY_PAID = "DDP"
    DELIVERED_DUTY_UNPAID = "DDU"
    DELIVERED_EX_QUAY = "DEQ"
    DELIVERED_EX_SHIP = "DES"
    EX_WORKS = "EXW"
    FREE_ALONGSIDE_SHIP = "FAS"
    FREE_CARRIER = "FCA"
    FREE_HOUSE = "FH"
    FREE_ON_BOARD = "FOB"
    NOT_FREE = "UN"


@dataclass
class SAPS4HANAPurchaseOrderDetails:
    """Represents the details of a purchase order in SAP S4 HANA."""

    purchase_order_number: str
    purchase_order_type: str
    created_by: str
    creation_date: str
    purchase_order_date: str
    supplier: str
    company_code: str
    purchasing_organization: str
    purchasing_group: str
    payment_terms: str
    document_currency: str
    exchange_rate: float


@dataclass
class SAPS4HANAPurchaseOrderLineItem:
    """Represents the details of a purchase order line item in SAP S4 HANA."""

    purchase_order: str
    purchase_order_item: str
    material: str
    order_quantity: float
    net_price_amount: float
    document_currency: str
    plant: str
    net_amount: Optional[float] = None
