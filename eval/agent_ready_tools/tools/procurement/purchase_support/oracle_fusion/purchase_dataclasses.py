from typing import List, Optional

from pydantic.dataclasses import dataclass


@dataclass
class OracleFusionSupplierPOTransmission:
    """Represents the supplier purchase transmission details in Oracle Fusion."""

    supplier_id: Optional[int]
    supplier_site_id: Optional[int]
    communication_method: Optional[str]
    supplier_fax: Optional[str]
    supplier_email: Optional[str]
    supplier_cc_email: Optional[str]
    supplier_bcc_email: Optional[str]


@dataclass
class OracleFusionPOSupplierDetails(OracleFusionSupplierPOTransmission):
    """Represents the supplier details for purchase order in Oracle Fusion."""

    supplier_name: Optional[str]
    supplier_site: Optional[str]
    supplier_contact: Optional[str]


@dataclass
class OracleFusionPurchaseOrderItem:
    """Represents a purchase order item details in Oracle Fusion."""

    po_line_id: Optional[int]
    line_number: Optional[int]
    item_name: Optional[str]
    item_description: Optional[str]
    quantity: Optional[int]
    item_value: Optional[int]
    currency: Optional[str]
    unit_of_measure: Optional[str]


@dataclass
class OracleFusionPurchaseOrderHeader:
    """Represents a list of purchase orders in Oracle Fusion."""

    purchase_order_id: int
    po_number: str
    description: Optional[str]
    supplier_name: Optional[str]
    ordered_amount: float
    currency: str
    creation_date: str
    status: str


@dataclass
class OracleFusionPurchaseOrderDetails(OracleFusionPurchaseOrderHeader):
    """Represents a purchase order in Oracle Fusion."""

    purchase_basis: str
    sold_to_legal_entity: str
    procurement_business_unit: str
    bill_to_business_unit: Optional[str]
    buyer: str
    requisition_number: Optional[int]
    tax_amount: int
    shipping_method: str
    payment_terms: Optional[str]
    shipping_address: Optional[str]
    billing_address: Optional[str]
    purchase_order_items: Optional[List[OracleFusionPurchaseOrderItem]]
    supplier_details: Optional[OracleFusionPOSupplierDetails]


@dataclass
class OracleFusionPurchaseRequisitionHeader:
    """Represents a list of purchase requisition in Oracle Fusion."""

    purchase_requisition_id: int
    requisition_number: str
    preparer: str
    description: Optional[str]
    document_status: Optional[str]
    creation_date: str
    fund_status: Optional[str]
    justification: Optional[str]


@dataclass
class OracleFusionPurchaseRequisitionItemBilling:
    """Represents the item billing details of a purchase requisition in Oracle Fusion."""

    requisition_distribution_id: Optional[int]
    distribution_number: Optional[int]
    billing_quantity: Optional[int]
    charge_account_id: Optional[int]
    charge_account: Optional[str]
    billing_amount: Optional[float]
    budget_date: Optional[str]


@dataclass
class OracleFusionPurchaseRequisitionLineDetails:
    """Represents a purchase requisition line details in Oracle Fusion."""

    requisition_line_id: Optional[int]
    line_number: Optional[int]
    category_name: Optional[str]
    item_description: Optional[str]
    item_id: Optional[int]
    item: Optional[str]
    quantity: Optional[int]
    requester: Optional[str]
    unit_price: Optional[int]
    unit_of_measure: Optional[str]
    price: Optional[int]
    line_status: Optional[str]
    purchase_order: Optional[str]
    deliver_to_location_code: Optional[str]
    destination_type: Optional[str]
    buyer: Optional[str]
    supplier_on_purchase_order: Optional[str]
    supplier_item_number: Optional[int]
    source_agreement: Optional[str]
    requested_delivery_date: Optional[str]
    billing_details: Optional[List[OracleFusionPurchaseRequisitionItemBilling]]


@dataclass
class OracleFusionPurchaseRequisitionDetails(OracleFusionPurchaseRequisitionHeader):
    """Represents a purchase requisition in Oracle Fusion."""

    requisitioning_business_unit_id: int
    requisitioning_business_unit: str
    preparer_id: int
    identification_key: Optional[str]
    requisition_line_group: Optional[str]
    taxation_country: Optional[str]
    purchase_requisition_items: Optional[List[OracleFusionPurchaseRequisitionLineDetails]]


@dataclass
class OracleFusionRequisitionCartItems:
    """Represents the cart items to add in requisitions from Oracle Fusion."""

    item_number: Optional[str]
    item_description: str
    category: str
    unit_of_measure: Optional[str]
    unit_price: float
    currency_code: str
    line_type: str


@dataclass
class OracleFusionSubmitPurchaseOrder:
    """Represents the response from Oracle Fusion after submitting a purchase order."""

    result: Optional[str]


@dataclass
class OracleFusionCreatePurchaseOrderResult:
    """Represents the result of a successful purchase order creation in Oracle Fusion."""

    purchase_order_id: int
    purchase_order_number: str
    procurement_business_unit: str
    requisitioning_business_unit: str
    buyer_email: str
    currency: str
    supplier: Optional[str]
    supplier_site: Optional[str]
    special_handling_type: Optional[str]
    default_ship_to_location: Optional[str]


@dataclass
class OracleFusionShipToLocationHeader:
    """Represents the list of ship-to locations from Oracle Fusion."""

    location_id: int
    location_name: str
    address: str


@dataclass
class OracleFusionSpecialHandlingTypesHeader:
    """Represents the list of special handling types from Oracle Fusion."""

    special_handling_type: str
    special_handling_type_code: str


@dataclass
class OracleFusionCurrencyHeader:
    """Represents the list of currencies from Oracle Fusion."""

    currency: str
    currency_code: str


@dataclass
class OracleFusionProcurementBUHeader:
    """Represents the list of procurement business units from Oracle Fusion."""

    procurement_business_unit_id: int
    procurement_business_unit: str
