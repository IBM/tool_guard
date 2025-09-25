from dataclasses import field
from typing import Any, Dict, Optional, Set, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.invoice_management.coupa.helper_functions_invoice_management import (
    coupa_build_invoice_from_response,
    coupa_build_receipt_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaInvoiceReceiptComparisonResult:
    """Class to store the result of comparing an Invoice with its multiple receipts."""

    invoice_id: int
    status: str
    message: str = ""
    po_number: Optional[str] = None
    line_items_match: Dict[str, bool] = field(default_factory=dict)
    total_amount_match: bool = False
    total_amount_discrepancies: Dict[str, float] = field(default_factory=dict)
    quantity_match: Dict[str, bool] = field(default_factory=dict)
    unit_price_match: Dict[str, bool] = field(default_factory=dict)
    line_item_discrepancies: Dict[str, Dict[str, Dict[str, Union[str, float, None]]]] = field(
        default_factory=dict
    )
    currency_match: Dict[str, bool] = field(default_factory=dict)
    description_match: Dict[str, bool] = field(default_factory=dict)
    overall_status: str = "APPROVED"


@dataclass
class InvoiceReceiptAggregatedData:
    """Helper class to store aggregated receipt data per order line."""

    quantity: float = 0.0
    total: float = 0.0
    prices: Set[float] = field(default_factory=set)
    currencies: Set[str] = field(default_factory=set)
    descriptions: Set[str] = field(default_factory=set)


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_invoice_receipt_matching(
    invoice_id: int,
) -> ToolResponse[CoupaInvoiceReceiptComparisonResult]:
    """
    Match an invoice with all its corresponding receipts.

    Aggregates receipt data per order line and compares with the invoice.

    Args:
        invoice_id: The invoice ID

    Returns:
        ToolResponse containing CoupaInvoiceReceiptComparisonResult with the results of comparison or error information.
    """
    try:
        client = get_coupa_client()
    except ValueError:
        return ToolResponse(success=False, message="Failure in retrieving credentials")

    invoice_response = client.get_request(resource_name=f"invoices/{invoice_id}")
    if "errors" in invoice_response:
        return ToolResponse(
            success=False, message=coupa_format_error_string(invoice_response), content=None
        )

    if not invoice_response:
        result = CoupaInvoiceReceiptComparisonResult(
            invoice_id=invoice_id,
            status="error",
            overall_status="error",
            message="Invoice not found.",
        )
        return ToolResponse(
            success=False, message=f"Invoice with ID {invoice_id} not found", content=result
        )

    invoice = coupa_build_invoice_from_response(invoice_response)
    if not invoice:
        result = CoupaInvoiceReceiptComparisonResult(
            invoice_id=invoice_id,
            status="error",
            overall_status="error",
            message="Invoice not found.",
        )
        return ToolResponse(
            success=False,
            message=f"Failed to build invoice from response for ID {invoice_id}",
            content=result,
        )

    po_number = next(
        (line.po_number for line in invoice.invoice_lines if line and line.po_number), None
    )

    if not po_number:
        result = CoupaInvoiceReceiptComparisonResult(
            invoice_id=invoice_id,
            status="error",
            overall_status="error",
            message="Purchase Order not found.",
        )
        return ToolResponse(
            success=False, message="Purchase Order not found in invoice lines", content=result
        )

    params = {"order-line[order-header-id]": po_number, "fields": '["id"]'}
    receipt_response = client.get_request_list(
        resource_name="receiving_transactions", params=params
    )
    if len(receipt_response) == 1 and "errors" in receipt_response[0]:
        return ToolResponse(
            success=False, message=coupa_format_error_string(receipt_response[0]), content=None
        )
    receipt_ids = [
        item.get("id")
        for item in receipt_response
        if isinstance(item, dict) and "id" in item and isinstance(item.get("id"), int)
    ]

    if not receipt_ids:
        result = CoupaInvoiceReceiptComparisonResult(
            invoice_id=invoice_id,
            po_number=str(po_number),
            status="BLOCKED",
            overall_status="BLOCKED",
            message=f"No receipts found for invoice {invoice_id}",
        )
        return ToolResponse(
            success=False, message=f"No receipts found for PO {po_number}", content=result
        )

    result = CoupaInvoiceReceiptComparisonResult(
        invoice_id=invoice_id,
        po_number=str(po_number),
        status="APPROVED",
        overall_status="APPROVED",
        message="All fields match.",
    )
    aggregated_data: Dict[str, InvoiceReceiptAggregatedData] = {}

    # Extract the invoice currency
    invoice_currency = invoice.currency.code if invoice.currency else ""

    # Process each receipt linked to the PO
    for receipt_id in receipt_ids:
        response = client.get_request(resource_name=f"receiving_transactions/{receipt_id}")

        if "errors" in response:
            return ToolResponse(
                success=False, message=coupa_format_error_string(response), content=None
            )

        if not response:
            continue

        receipt = coupa_build_receipt_from_response(response)
        if not receipt or receipt.status == "voided":
            continue

        items = getattr(receipt, "items", [receipt])

        for item in items:
            order_line = getattr(item, "order_line", None)
            order_line_id = order_line.get("id") if isinstance(order_line, dict) else order_line
            if not order_line_id:
                continue
            key = str(order_line_id)
            price = float(getattr(item, "price", 0) or 0)
            quantity_val = float(getattr(item, "quantity", 0) or 0)
            total_val = float(getattr(item, "total", 0) or 0)
            price_val = round(price, 2)

            currency_code: Optional[str] = None
            try:
                currency_code = (
                    item.account.account_type.currency.code
                    if item.account
                    and item.account.account_type
                    and item.account.account_type.currency
                    else None
                )
            except AttributeError:
                pass

            if key not in aggregated_data:
                aggregated_data[key] = InvoiceReceiptAggregatedData()

            aggregated_data[key].quantity += quantity_val
            aggregated_data[key].total += total_val
            aggregated_data[key].prices.add(price_val)
            if currency_code:
                aggregated_data[key].currencies.add(currency_code)

            description = (
                order_line.get("description", "").strip() if isinstance(order_line, dict) else ""
            )
            if description:
                aggregated_data[key].descriptions.add(description)

    # Compare against invoice lines
    invoice_total = 0.0
    receipts_total = 0.0
    discrepancies_summary = []

    for line in invoice.invoice_lines:
        if line is None:
            continue
        order_line_id = str(line.order_line_id)
        if order_line_id not in aggregated_data:
            result.line_item_discrepancies[order_line_id] = {
                "error": {"message": "No matching receipts."}
            }
            result.status = "BLOCKED"
            result.overall_status = "BLOCKED"
            discrepancies_summary.append(f"Missing receipts for order line {order_line_id}")
            continue

        agg = aggregated_data[order_line_id]
        invoice_total += float(line.total or 0)
        receipts_total += agg.total
        discrepancies: Dict[str, Dict[str, Any]] = {}

        # Quantity Match
        invoice_quantity = float(line.quantity or 0.0)
        if abs(invoice_quantity - agg.quantity) > 0.01:
            discrepancies["quantity"] = {
                "invoice": invoice_quantity,
                "receipts": agg.quantity,
            }
            discrepancies_summary.append(f"Quantity mismatch on line {order_line_id}")
        else:
            result.quantity_match[order_line_id] = True

        # Unit Price Match
        invoice_price = float(line.price or 0.0)
        if len(agg.prices) != 1 or abs(invoice_price - list(agg.prices)[0]) > 0.01:
            discrepancies["unit_price"] = {
                "invoice": invoice_price,
                "receipts": list(agg.prices),
            }
            discrepancies_summary.append(f"Unit price mismatch on line {order_line_id}")
        else:
            result.unit_price_match[order_line_id] = True

        # Currency Match
        if len(agg.currencies) > 1 or (invoice_currency and invoice_currency not in agg.currencies):
            discrepancies["currency"] = {
                "invoice": invoice_currency,
                "receipts": list(agg.currencies),
            }
            discrepancies_summary.append(f"Currency mismatch on line {order_line_id}")

        # Description Match
        invoice_description = line.description.strip() if line.description else ""
        if len(agg.descriptions) > 1 or invoice_description not in agg.descriptions:
            discrepancies["description"] = {
                "invoice": invoice_description,
                "receipts": list(agg.descriptions),
            }
            discrepancies_summary.append(f"Description mismatch on line {order_line_id}")

        if discrepancies:
            result.line_item_discrepancies[order_line_id] = discrepancies
            result.status = "BLOCKED"
            result.overall_status = "BLOCKED"

    # If no discrepancies were found, status remains "APPROVED"
    if not result.line_item_discrepancies:
        result.status = "APPROVED"
        result.overall_status = "APPROVED"
        # Check total amount match
        if abs(invoice_total - receipts_total) <= 0.01:
            result.total_amount_match = True
        else:
            result.total_amount_discrepancies = {
                "invoice": invoice_total,
                "receipts": receipts_total,
            }
            result.status = "BLOCKED"
            result.overall_status = "BLOCKED"
            discrepancies_summary.append("Total amount mismatch")

    # Set final message based on discrepancies
    result.message = (
        "All fields match, no action needed"
        if result.status == "APPROVED"
        else "\n".join(discrepancies_summary)
    )

    return ToolResponse(
        success=True, message="Invoice-receipt matching completed successfully", content=result
    )
