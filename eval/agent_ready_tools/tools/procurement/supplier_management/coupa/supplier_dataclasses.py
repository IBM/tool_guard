from enum import StrEnum
from typing import List, Optional

from pydantic.dataclasses import dataclass


class CoupaAddressPurposeType(StrEnum):
    """Represents the address purpose type in Coupa."""

    BRANCH = "branch"
    FRANCHISE = "franchise"
    HOME = "Home"
    HQ = "hq"
    MAILING = "Mailing"
    OTHER = "Other"
    OTHER_ADDRESS = "other_address"
    SERVICE_CENTER = "service_center"
    WAREHOUSE = "warehouse"
    WORK = "Work"


class ContactPurposeType(StrEnum):
    """Represents the contact purpose type in Coupa."""

    ACCORDING = "accounting_contact"
    DIVERSITY = "diversity_contact"
    LEGAL = "legal_contact"
    PROCUREMENT = "procurement_contact"
    RISK = "risk_contact"
    SALES = "sales_contact"
    SOURCING = "sourcing"
    SERVICE_DESK = "service_desk_contact"
    OTHER = "other_contact"
    EXECUTIVE = "executive_contact"


class CoupaPurchaseOrderType(StrEnum):
    """The purchase order transmission method in Coupa."""

    CXML = "cxml"
    XML = "xml"
    EMAIL = "email"
    PROMPT = "prompt"
    MARK_AS_SENT = "mark_as_sent"
    BUY_ONLINE = "buy_online"


class InvoiceMatchingLevel(StrEnum):
    """The invoice matching level in Coupa."""

    TWO_WAY = "2-way"
    THREE_WAY = "3-way"
    THREE_WAY_DIRECT = "3-way-direct"
    NONE = "none"


@dataclass
class CoupaContact:
    """Represents a contact in Coupa."""

    email: Optional[str]
    name_given: Optional[str]
    name_family: Optional[str]
    reference_code: Optional[str]


@dataclass
class CoupaBaseAddress:
    """Represents the base address in Coupa."""

    # some address have a faulty None value
    street1: str
    street2: Optional[str]
    city: str
    state: Optional[str]
    postal_code: str
    country: str
    name: Optional[str]


@dataclass
class CoupaContactAddress(CoupaBaseAddress):
    """Represents a contact address in Coupa."""

    location_code: Optional[str] = None


@dataclass
class CoupaRemitToAddress(CoupaBaseAddress):
    """Represents a remit-to-address in Coupa."""

    remit_to_address_id: int
    remit_to_code: Optional[str] = None
    active: Optional[bool] = None


@dataclass
class CoupaSupplierItem:
    """Represents a supplier item in Coupa."""

    item_id: str
    supplier_item_id: str
    supplier_id: int
    supplier_part_num: str
    price: float
    preferred: bool
    currency_code: str


@dataclass
class CoupaSupplierItemDetails:
    """Represents a supplier item in Coupa."""

    supplier_id: int
    supplier_name: str
    supplier_number: Optional[str]
    item_id: int
    item_name: str
    item_number: Optional[str] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None
    storage_quantity: Optional[int] = None
    consumption_quantity: Optional[int] = None


@dataclass
class CoupaSupplierDetails:
    """Represents a supplier details in Coupa."""

    id: int
    status: str
    name: str
    contact_email: Optional[str]
    number: Optional[str]


@dataclass
class CoupaSupplierContactDetails(CoupaContact):
    """Represents a supplier's contact details in Coupa."""

    contact_id: int
    purpose: Optional[str] = None


@dataclass
class CoupaSupplierTaxRegistration:
    """Represents a supplier's tax registration in Coupa."""

    id: int
    number: str
    active: bool
    country: str


@dataclass
class CreateSupplierResult:
    """Represents the result of creating a supplier in Coupa."""

    id: int


@dataclass
class CreateRemitToAddressResult:
    """Represents the result of creating a remit-to-address in Coupa."""

    id: int


@dataclass
class CreateSupplierItemResult:
    """Represents the result of creating a supplier item in Coupa."""

    item_id: int
    supplier_id: int
    supplier_item_id: int


@dataclass
class CoupaSupplierAddressDetails(CoupaBaseAddress):
    """Represents a supplier's address details in Coupa."""

    address_id: int
    purpose: Optional[str] = None


@dataclass
class CoupaSupplierDetailsResponse:
    """Represents a supplier's details in Coupa."""

    supplier_details: CoupaSupplierDetails
    contact_details: List[CoupaSupplierContactDetails]
    address_details: List[CoupaSupplierAddressDetails]
