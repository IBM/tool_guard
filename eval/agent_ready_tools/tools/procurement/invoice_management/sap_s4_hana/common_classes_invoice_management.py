from enum import StrEnum
from typing import List, Optional

from pydantic.dataclasses import dataclass


@dataclass
class S4HANAInvoicePayment:
    """Represents Payment details of an invoice in SAP S4 HANA."""

    invoice_id: str
    fiscal_year: str
    due_calculation_base_date: Optional[str] = None
    manual_cash_discount: Optional[str] = None
    cash_discount_1_percent: Optional[str] = None
    cash_discount_1_days: Optional[str] = None
    cash_discount_2_percent: Optional[str] = None
    cash_discount_2_days: Optional[str] = None
    net_payment_days: Optional[str] = None
    invoice_reference: Optional[str] = None
    payment_terms: Optional[str] = None
    payment_blocking_reason: Optional[str] = None


@dataclass
class S4HANAInvoiceTax:
    """Represents Tax details of an invoice in SAP S4 HANA."""

    invoice_id: str
    fiscal_year: str
    tax_code: Optional[str] = None
    currency: Optional[str] = None
    tax_amount: Optional[str] = None


@dataclass
class S4HANAInvoiceSupplier:
    """Represents a Vendor of an invoice in SAP S4 HANA."""

    invoice_id: str
    fiscal_year: str
    invoicing_party: Optional[str] = None
    postal_code: Optional[str] = None
    city_name: Optional[str] = None
    country: Optional[str] = None
    street_address_name: Optional[str] = None


@dataclass
class S4HANAInvoicePurchaseOrder:
    """Represents a supplier invoice in SAP S4 HANA."""

    invoice_id: str
    fiscal_year: str
    supplier_invoice_item: Optional[str] = None
    purchase_order: Optional[str] = None
    purchase_order_item: Optional[str] = None
    plant: Optional[str] = None
    reference_document: Optional[str] = None
    reference_document_fiscal_year: Optional[str] = None
    reference_document_item: Optional[str] = None
    tax_code: Optional[str] = None
    supplier_invoice_item_amount: Optional[str] = None
    currency: Optional[str] = None
    quantity_in_purchase_order_unit: Optional[str] = None


@dataclass
class S4HANAInvoiceLineItems:
    """Represents a supplier invoice in SAP S4 HANA."""

    invoice_id: str
    fiscal_year: str
    supplier_invoice_item: Optional[str] = None
    purchase_order: Optional[str] = None
    purchase_order_item: Optional[str] = None
    plant: Optional[str] = None
    currency: Optional[str] = None
    quantity_in_purchase_order_unit: Optional[str] = None


@dataclass
class SAPS4HANAInvoice:
    """Represents an invoice in SAP S4 HANA."""

    invoice_id: str
    fiscal_year: str
    company_code: Optional[str] = None
    invoice_date: Optional[str] = None
    posting_date: Optional[str] = None
    invoice_gross_amount: Optional[str] = None
    currency: Optional[str] = None
    due_calculation_base_date: Optional[str] = None
    status: Optional[str] = None
    creation_date: Optional[str] = None
    assignment: Optional[str] = None
    accounting_document_type: Optional[str] = None
    supplier: Optional[str] = None
    document_number: Optional[str] = None
    invoice_header: Optional[str] = None
    payment_terms: Optional[str] = None
    invoice_reference: Optional[str] = None
    payment: Optional[S4HANAInvoicePayment] = None
    tax_results: Optional[List[S4HANAInvoiceTax]] = None
    vendor: Optional[S4HANAInvoiceSupplier] = None
    purchase_order: Optional[List[S4HANAInvoicePurchaseOrder]] = None
    line_items: Optional[List[S4HANAInvoiceLineItems]] = None


class S4HANAInvoicePaymentmethod(StrEnum):
    """Enum specifying the payment method for invoices in SAP S4 HANA."""

    CHECK = "C"
    BANK_TRANSFER_ACH_CCD = "D"
    BANK_TRANSFER_ACH_PPD = "P"
    BANK_TRANSFER_ACH_CTX = "T"
