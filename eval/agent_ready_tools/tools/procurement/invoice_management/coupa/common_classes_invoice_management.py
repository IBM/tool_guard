from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, List, Optional

from pydantic.dataclasses import dataclass


@dataclass
class CoupaInvoicePerson:
    """Represents a person in an invoice on Coupa."""

    id: int
    login: Optional[str] = None
    email: Optional[str] = None
    employee_number: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    fullname: Optional[str] = None
    salesforce_id: Optional[str] = None
    avatar_thumb_url: Optional[str] = None
    assignee: Optional[str] = None


@dataclass
class CoupaInvoiceCountry:
    """Represents a country in an invoice on Coupa."""

    id: int
    code: str  # 2-digit country code
    name: str  # country name


@dataclass
class CoupaInvoiceAddress:
    """Represent an adresss in an invoice on Coupa."""

    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    name: Optional[str] = None
    location_code: Optional[str] = None
    street1: Optional[str] = None
    street2: Optional[str] = None
    street3: Optional[str] = None
    street4: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    attention: Optional[str] = None
    active: bool = False
    business_group_name: Optional[str] = None
    vat_number: Optional[str] = None
    local_tax_number: Optional[str] = None
    type: Optional[str] = None
    address_type: Optional[str] = None
    default: Optional[bool] = None
    custom_fields: Optional[Any] = None
    country: Optional[CoupaInvoiceCountry] = None
    vat_country: Optional[CoupaInvoiceCountry] = None


@dataclass
class CoupaInvoiceSupplierContact:
    """Represents a supplier contact in an invoice on Coupa."""

    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    email: Optional[str] = None
    name_prefix: Optional[str] = None
    name_suffix: Optional[str] = None
    name_additional: Optional[str] = None
    name_given: Optional[str] = None
    name_family: Optional[str] = None
    name_fullname: Optional[str] = None
    notes: Optional[str] = None
    active: bool = False
    business_group_name: Optional[str] = None
    vat_number: Optional[str] = None
    local_tax_number: Optional[str] = None
    type: Optional[str] = None
    created_by: Optional[CoupaInvoicePerson] = None
    updated_by: Optional[CoupaInvoicePerson] = None
    primary_address: Optional[CoupaInvoiceAddress] = None


@dataclass
class CoupaInvoiceSupplier:
    """Represents a supplier in an invoice on Coupa."""

    id: int
    name: Optional[str] = None
    display_name: Optional[str] = None
    number: Optional[str] = None
    risk_level: Optional[str] = None
    custom_fields: Optional[Any] = None
    primary_contact: Optional[CoupaInvoiceSupplierContact] = None
    primary_address: Optional[CoupaInvoiceAddress] = None
    created_by: Optional[CoupaInvoicePerson] = None
    updated_by: Optional[CoupaInvoicePerson] = None


@dataclass
class CoupaInvoiceCurrency:
    """Represent a currency in an invoice on Coupa."""

    id: int
    code: str
    decimals: int
    updated_by: Optional[CoupaInvoicePerson] = None


def convert_datetime_to_iso_str(dt: Optional[datetime]) -> str:
    """
    convert datetime to a str in iso format with time zone.

    Args:
        dt: datetime as an input

    Returns:
        str as an output
    """
    if dt is None:
        return ""
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S %z")
    return f"{dt_str[:-2]}:{dt_str[-2:]}"


def convert_string_to_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    """
    convert a datetime in json to a date/time string in ISO format.

    Args:
        dt_str: a datetime string or None

    Returns:
        a datetime object or None
    """
    if not dt_str:
        return None
    return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S%z")


def show(obj: Optional[Any]) -> str:
    """
    this is for mypd claiming errors when using f-string in a string where the object in the
    f-string is Optional[something] if the object is None, return am empyty string. otherwise return
    str(obj)

    Args:
        obj: an object

    Returns:
        "" or str(obj)
    """
    if obj is None:
        return ""
    else:
        return str(obj)


@dataclass
class CoupaInvoicePaymentTerm:
    """Represent a payment term in an invoice on Coupa."""

    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    days_for_net_payment: Optional[int] = None
    days_for_discount_payment: Optional[int] = None
    discount_rate: Optional[float] = None
    active: bool = False
    type: Optional[str] = None
    net_cutoff_day: Optional[int] = None
    net_due_month: Optional[int] = None
    net_due_day: Optional[int] = None
    discount_cutoff_day: Optional[int] = None
    discount_due_month: Optional[int] = None
    discount_due_day: Optional[int] = None
    content_groups: Optional[Any] = None
    updated_by: Optional[CoupaInvoicePerson] = None
    remit_to_address: Optional[CoupaInvoiceAddress] = None


@dataclass
class CoupaInvoiceAccountType:
    """Represent an account type in an invoice on Coupa."""

    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    name: Optional[str] = None
    active: bool = False
    legal_entity_name: Optional[str] = None
    dynamic_flag: bool = False
    currency: Optional[CoupaInvoiceCurrency] = None
    primary_address: Optional[CoupaInvoiceAddress] = None
    created_by: Optional[CoupaInvoicePerson] = None
    updated_by: Optional[CoupaInvoicePerson] = None


@dataclass
class CoupaInvoiceAccount:
    """Represent an account in an invoice on Coupa."""

    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    active: Optional[bool] = None
    account_type_id: Optional[int] = None
    # segment_1: Optional[str] = None
    # segment_2: Optional[str] = None
    # segment_3: Optional[str] = None
    # segment_4: Optional[str] = None
    # segment_5: Optional[str] = None
    # segment_6: Optional[str] = None
    # segment_7: Optional[str] = None
    # segment_8: Optional[str] = None
    # segment_9: Optional[str] = None
    # segment_10: Optional[str] = None
    # segment_11: Optional[str] = None
    # segment_12: Optional[str] = None
    # segment_13: Optional[str] = None
    # segment_14: Optional[str] = None
    # segment_15: Optional[str] = None
    # segment_16: Optional[str] = None
    # segment_17: Optional[str] = None
    # segment_18: Optional[str] = None
    # segment_19: Optional[str] = None
    # segment_20: Optional[str] = None
    account_type: Optional[CoupaInvoiceAccountType] = None
    created_by: Optional[CoupaInvoicePerson] = None
    updated_by: Optional[CoupaInvoicePerson] = None


@dataclass
class CoupaInvoiceCommodity:
    """Represent a commodity in an invoice on Coupa."""

    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    active: bool = False
    name: Optional[str] = None
    translated_name: Optional[str] = None
    deductibility: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    imported_from_taxonomy: bool = False
    gl: Optional[str] = None
    common_gl_acct: Optional[Any] = None
    parent: Optional[Any] = None
    created_by: Optional[CoupaInvoicePerson] = None
    updated_by: Optional[CoupaInvoicePerson] = None


@dataclass
class CoupaInvoiceItem:
    """Represent an item in an invoice on Coupa."""

    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    description: Optional[str] = None
    item_number: Optional[str] = None
    name: Optional[str] = None
    active: bool = False
    storage_quantity: Optional[str] = None
    image_url: Optional[str] = None
    manufacturer_name: Optional[str] = None
    manufacturer_part_number: Optional[str] = None
    item_type: Optional[str] = None
    pack_qty: Optional[str] = None
    pack_weight: Optional[str] = None
    pack_uom_idy: Optional[str] = None
    receive_catch_weight: Optional[bool] = None
    allow_partial_quantity: bool = False
    inventory_lot_tracking_enabled: Optional[bool] = False
    inventory_lot_expiration_type: Optional[str] = None
    commodity: Optional[CoupaInvoiceCommodity] = None


@dataclass
class CoupaInvoiceUOM:
    """Represent a unit of measure in an invoice on Coupa."""

    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None
    allowable_precision: Optional[int] = None
    active: bool = False
    updated_by: Optional[CoupaInvoicePerson] = None


@dataclass
class CoupaInvoiceLine:
    """Represent an invoice line on Coupa."""

    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    account: Optional[CoupaInvoiceAccount] = None
    account_allocations: Optional[Any] = None
    accounting_total: Optional[str] = None
    description: Optional[str] = None
    line_num: Optional[int] = None
    order_header_num: Optional[int] = None
    po_number: Optional[int] = None
    order_line_id: Optional[int] = None
    order_line_num: Optional[str] = None
    price: Optional[str] = None
    net_weight: Optional[str] = None
    price_per_uom: Optional[str] = None
    quantity: Optional[str] = None
    adjustment_type: Optional[str] = None
    status: Optional[str] = None
    tax_rate: Optional[str] = None
    tax_location: Optional[str] = None
    tax_amount: Optional[str] = None
    tax_description: Optional[str] = None
    tax_supply_date: Optional[str] = None
    total: Optional[str] = None
    type: Optional[str] = None
    tax_amount_engine: Optional[str] = None
    tax_code_engine: Optional[str] = None
    tax_rate_engine: Optional[str] = None
    tax_distribution_total: Optional[str] = None
    shipping_distribution_total: Optional[str] = None
    handling_distribution_total: Optional[str] = None
    misc_distribution_total: Optional[str] = None
    match_reference: Optional[str] = None
    original_date_of_supply: Optional[str] = None
    delivery_note_number: Optional[str] = None
    discount_amount: Optional[str] = None
    company_uom: Optional[str] = None
    property_tax_account: Optional[str] = None
    source_part_num: Optional[str] = None
    supp_aux_part_num: Optional[str] = None
    customs_declaration_number: Optional[str] = None
    hsn_sac_code: Optional[str] = None
    unspsc: Optional[str] = None
    billing_note: Optional[str] = None
    fiscal_code: Optional[str] = None
    classification_of_goods: Optional[str] = None
    municipality_taxation_code: Optional[str] = None
    item_barcode: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    deductibility: Optional[str] = None
    custom_fields: Optional[Any] = None
    accounting_total_currency: Optional[CoupaInvoiceCurrency] = None
    currency: Optional[CoupaInvoiceAccount] = None
    item: Optional[CoupaInvoiceItem] = None
    uom: Optional[CoupaInvoiceUOM] = None  # Unit of Measure
    order_line_commodity: Optional[Dict] = None
    order_line_custom_fields: Optional[Dict] = None
    period: Optional[Dict] = None
    contract: Optional[Dict] = None
    tax_lines: Optional[List] = None
    withholding_tax_lines: Optional[List] = None
    tags: Optional[List] = None
    taggings: Optional[List] = None
    failed_tolerances: Optional[List] = None
    commodity: Optional[CoupaInvoiceCommodity] = None
    created_by: Optional[CoupaInvoicePerson] = None
    updated_by: Optional[CoupaInvoicePerson] = None


@dataclass
class CoupaInvoiceHeader:
    """Represents a invoice in coupa."""

    invoice_id: int
    invoice_number: str
    supplier_name: str
    net_due_date: str
    total_amount: str
    currency: str
    status: str
    created_at: str


@dataclass
class CoupaInvoicesResponse:
    """Represents the response from getting all invoices in Coupa."""

    invoices: List[CoupaInvoiceHeader]


@dataclass
class InvoiceStatus(StrEnum):
    """Enum specifying the status for invoices in Coupa."""

    NEW = "new"
    AP_HOLD = "ap_hold"
    DRAFT = "draft"
    ON_HOLD = "on_hold"
    PENDING_RECEIPT = "pending_receipt"
    REJECTED = "rejected"
    ABANDONED = "abandoned"
    DISPUTED = "disputed"
    PENDING_APPROVAL = "pending_approval"
    BOOKING_HOLD = "booking_hold"
    PENDING_ACTION = "pending_action"
    APPROVED = "approved"
    VOIDED = "voided"
    PROCESSING = "processing"
    INVALID = "invalid"
    PAYABLE_ADJUSTMENT = "payable_adjustment"


@dataclass
class CoupaComments:
    """Represents a general comment in Coupa."""

    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    commentable_id: Optional[int] = None
    commentable_type: Optional[str] = None
    reason_code: Optional[str] = None
    to_supplier: Optional[str] = None
    comment_type: Optional[str] = None
    comments: Optional[str] = None
    comments_with_mentions_uniq_id: Optional[str] = None
    allow_edit: Optional[bool] = None
    allow_delete: Optional[bool] = None
    is_read: Optional[bool] = None
    modified: Optional[bool] = None
    attachments: Optional[List[Any]] = None
    mentionees: Optional[List[Any]] = None
    created_by: Optional[CoupaInvoicePerson] = None
    updated_by: Optional[CoupaInvoicePerson] = None


@dataclass
class CoupaCommentsList:
    """Represents a list of general comments in Coupa."""

    comments_list: List[CoupaComments]


@dataclass
class CoupaReceipt:
    """Represents a receipt in Coupa."""

    id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    barcode: Optional[str] = None
    price: Optional[str] = None
    quantity: Optional[str] = None
    rfid_tag: Optional[str] = None
    total: Optional[str] = None
    transaction_date: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    exported: Optional[bool] = None
    last_exported_at: Optional[str] = None
    receipts_batch_id: Optional[int] = None
    received_weight: Optional[str] = None
    match_reference: Optional[str] = None
    original_transaction_id: Optional[str] = None
    voided_value: Optional[str] = None
    account: Optional[CoupaInvoiceAccount] = None
    account_allocations: Optional[List] = None
    order_line: Optional[Any] = None
    item: Optional[CoupaInvoiceItem] = None
    to_warehouse_location: Optional[Dict] = None
    uom: Optional[Any] = None
    asset_tags: Optional[List] = None
    attachments: Optional[List] = None
    inventory_transaction_valuations: Optional[List] = None
    inventory_transaction_lots: Optional[List] = None
    current_integration_history_records: Optional[List] = None
    created_by: Optional[CoupaInvoicePerson] = None
    updated_by: Optional[CoupaInvoicePerson] = None


@dataclass
class CoupaReceiptHeader:
    """Represents a receipt with only the most important fields in Coupa."""

    id: int
    purchase_order_id: Optional[int] = None
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    price: Optional[str] = None
    quantity: Optional[str] = None
    total: Optional[str] = None
    transaction_date: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    uom: Optional[Any] = None
    account: Optional[CoupaInvoiceAccount] = None
    order_line: Optional[Any] = None
    item: Optional[CoupaInvoiceItem] = None


@dataclass
class CoupaInvoice:
    """Represents an invoice."""

    id: int
    invoice_lines: List[CoupaInvoiceLine]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_number: Optional[str] = None
    status: Optional[str] = None
    payment_term: Optional[CoupaInvoicePaymentTerm] = None
    net_due_date: Optional[str] = None
    compliant: bool = False
    supplier: Optional[CoupaInvoiceSupplier] = None
    remit_to_address: Optional[CoupaInvoiceAddress] = None
    internal_note: Optional[str] = None
    line_level_taxation: bool = False
    currency: Optional[CoupaInvoiceCurrency] = None
    shipping_amount: Optional[float] = None
    handling_amount: Optional[float] = None
    misc_amount: Optional[float] = None
    tax_amount: Optional[str] = None
    total_with_taxes: Optional[str] = None
    gross_total: Optional[str] = None
    paid: Optional[bool] = None
    payment_date: Optional[str] = None
    payment_notes: Optional[str] = None


@dataclass
class CoupaPOReceipt:
    """Represent a PO Receipt."""

    order_id: int
    line_id: Optional[int] = None
    line_number: Optional[str] = None
    description: Optional[str] = None
    receipt_id: Optional[int] = None
    receipt_status: Optional[str] = None
    created_at: Optional[str] = None
    order_price: Optional[str] = None
    receipt_price: Optional[str] = None
    order_quantity: Optional[str] = None
    receipt_quantity: Optional[str] = None
