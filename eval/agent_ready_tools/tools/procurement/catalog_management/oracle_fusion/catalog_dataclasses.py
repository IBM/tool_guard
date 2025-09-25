from typing import List, Optional

from pydantic.dataclasses import dataclass


@dataclass
class OracleFusionApprovedSupplierListEntry:
    """Represents a singular approved supplier list entry in Oracle Fusion."""

    asl_id: int
    procurement_business_unit_id: int
    procurement_business_unit: str
    scope: str
    ship_to_organization: Optional[str]  # optional if scope is global
    item: str
    item_id: int
    supplier: str
    supplier_id: int
    supplier_site: Optional[str]
    supplier_site_id: Optional[int]
    supplier_primary_vendor_item: Optional[str]
    status: str
    review_due_date: Optional[str]
    comments: Optional[str]
    created_at: str
    purchasing_uom: Optional[str]
    country_name: Optional[str]
    minimum_order_quantity: Optional[int]
    fixed_lot_multiple: Optional[int]


@dataclass
class OracleFusionApprovedSupplierListEntryList:
    """Represents a list of approved supplier list entries in Oracle Fusion."""

    supplier_list_entry_list: List[OracleFusionApprovedSupplierListEntry]


@dataclass
class OracleFusionItem:
    """Represents the core details of an item in Oracle Fusion."""

    organization_code: str
    item_number: str
    item_id: int
    item_description: str
    item_status: Optional[str]
    lifecycle_phase: Optional[str]
    item_class: str
    primary_uom_value: Optional[str]


@dataclass
class OracleFusionItemClass:
    """Represents a single Item Class detail from Oracle Fusion."""

    item_class_name: str
    description: Optional[str] = None
    item_class_id: Optional[int] = None


@dataclass
class OracleFusionUOM:
    """Represents a single Unit of Measure detail from Oracle Fusion."""

    uom_code: str
    description: Optional[str] = None
    uom_class_name: Optional[str] = None
    base_unit_flag: Optional[bool] = None
