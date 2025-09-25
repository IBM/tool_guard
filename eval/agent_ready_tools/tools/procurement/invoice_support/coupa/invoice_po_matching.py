"""This module provides functionality for matching invoices with purchase orders."""

from dataclasses import field
from typing import Any, Dict

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.invoice_management.coupa.helper_functions_invoice_management import (
    coupa_build_invoice_from_response,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_purchase_order_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaPOComparisonResult:
    """Dataclass to store the comparison results between invoice and PO."""

    invoice_id: int
    po_id: int
    status: str
    message: str
    line_items_match: Dict[str, bool] = field(default_factory=dict)
    total_amount_match: bool = False
    total_amount_discrepancies: Dict[str, float] = field(default_factory=dict)
    quantity_match: Dict[str, bool] = field(default_factory=dict)
    unit_price_match: Dict[str, bool] = field(default_factory=dict)
    line_total_match: Dict[str, bool] = field(default_factory=dict)
    currency_match: Dict[str, bool] = field(default_factory=dict)
    line_item_discrepancies: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_invoice_po_matching(invoice_id: int, po_id: int) -> ToolResponse[CoupaPOComparisonResult]:
    """
    Match an invoice with its corresponding purchase order.

    Args:
        invoice_id: The ID of the invoice.
        po_id: The ID of the purchase_order.

    Returns:
        ToolResponse containing CoupaPOComparisonResult with the results of comparison or error information.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request(resource_name=f"invoices/{invoice_id}")

    if "errors" in response:
        return ToolResponse(
            success=False, message=coupa_format_error_string(response), content=None
        )

    if not response:
        result = CoupaPOComparisonResult(
            invoice_id=invoice_id,
            po_id=po_id,
            status="error",
            message=f"Invoice with ID {invoice_id} not found. Please provide a valid invoice ID.",
        )
        return ToolResponse(
            success=False, message=f"Invoice with ID {invoice_id} not found", content=result
        )

    invoice = coupa_build_invoice_from_response(response)

    if not invoice:
        result = CoupaPOComparisonResult(
            invoice_id=invoice_id,
            po_id=po_id,
            status="error",
            message=f"Invoice with ID {invoice_id} not found. Please provide a valid invoice ID.",
        )
        return ToolResponse(
            success=False,
            message=f"Failed to build invoice from response for ID {invoice_id}",
            content=result,
        )

    response = client.get_request(resource_name=f"purchase_orders/{po_id}")
    if "errors" in response:
        return ToolResponse(
            success=False, message=coupa_format_error_string(response), content=None
        )

    if not response:
        result = CoupaPOComparisonResult(
            invoice_id=invoice_id,
            po_id=po_id,
            status="error",
            message=f"Purchase Order with ID {po_id} not found. Please provide a valid PO ID.",
        )
        return ToolResponse(
            success=False, message=f"Purchase Order with ID {po_id} not found", content=result
        )

    po = coupa_build_purchase_order_from_response(response)

    if not po:
        result = CoupaPOComparisonResult(
            invoice_id=invoice_id,
            po_id=po_id,
            status="error",
            message=f"Purchase Order with ID {po_id} not found. Please provide a valid PO ID.",
        )
        return ToolResponse(
            success=False,
            message=f"Failed to build purchase order from response for ID {po_id}",
            content=result,
        )

    # Initialize result
    result = CoupaPOComparisonResult(
        invoice_id=invoice_id,
        po_id=po_id,
        status="APPROVED",
        message="All fields match, no action needed",
    )

    # Extract currencies for comparison
    invoice_currency = invoice.currency.code if invoice.currency else ""
    po_currency = po.currency if po.currency else ""

    # Compare line items
    invoice_lines = invoice.invoice_lines
    po_lines = po.order_lines.order_lines

    # Create dictionaries for easier lookup
    po_lines_dict = {line.order_line_id: line for line in po_lines}
    invoice_lines_dict = {line.order_line_id: line for line in invoice_lines}

    # Compare each line item
    for line_num, invoice_line in invoice_lines_dict.items():
        po_line = po_lines_dict.get(line_num or -1)
        if not po_line:
            result.line_items_match[str(line_num)] = False
            result.line_item_discrepancies[str(line_num)] = {"error": "Line item not found in PO"}
            result.status = "BLOCKED"
            result.message = "Discrepancies found requiring review"
            continue

        # Compare quantities
        invoice_quantity = float(invoice_line.quantity or 0)
        po_quantity = float(po_line.quantity or 0)
        result.quantity_match[str(line_num)] = invoice_quantity == po_quantity

        # Compare unit prices
        invoice_price = float(invoice_line.price or 0)
        po_price = float(po_line.price or 0)
        result.unit_price_match[str(line_num)] = invoice_price == po_price

        # Compare line totals
        invoice_line_total = float(invoice_line.total or 0)
        po_line_total = float(po_line.total or 0)
        result.line_total_match[str(line_num)] = invoice_line_total == po_line_total

        # Compare currencies
        result.currency_match[str(line_num)] = invoice_currency == po_currency

        # Overall line item match
        result.line_items_match[str(line_num)] = (
            result.quantity_match[str(line_num)]
            and result.unit_price_match[str(line_num)]
            and result.line_total_match[str(line_num)]
            and result.currency_match[str(line_num)]
        )

        # Store discrepancies if any
        if not result.line_items_match[str(line_num)]:
            result.line_item_discrepancies[str(line_num)] = {
                "quantity": (
                    {
                        "invoice": invoice_quantity,
                        "po": po_quantity,
                    }
                    if not result.quantity_match[str(line_num)]
                    else None
                ),
                "unit_price": (
                    {
                        "invoice": invoice_price,
                        "po": po_price,
                    }
                    if not result.unit_price_match[str(line_num)]
                    else None
                ),
                "line_total": (
                    {
                        "invoice": invoice_line_total,
                        "po": po_line_total,
                    }
                    if not result.line_total_match[str(line_num)]
                    else None
                ),
                "currency": (
                    {
                        "invoice": invoice_currency,
                        "po": po_currency,
                    }
                    if not result.currency_match[str(line_num)]
                    else None
                ),
            }
            result.status = "BLOCKED"
            result.message = "Discrepancies found requiring review"

    # Compare total amounts
    invoice_total = float(invoice.total_with_taxes or 0)
    po_total = float(po.total_with_estimated_tax or 0)
    result.total_amount_match = invoice_total == po_total

    if not result.total_amount_match:
        result.total_amount_discrepancies = {
            "invoice": invoice_total,
            "po": po_total,
            "difference": invoice_total - po_total,
        }
        result.status = "BLOCKED"
        result.message = "Discrepancies found requiring review"

    return ToolResponse(
        success=True, message="Invoice-PO matching completed successfully", content=result
    )
