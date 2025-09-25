from dataclasses import field
from typing import Dict, Optional, Set, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.invoice_management.coupa.helper_functions_invoice_management import (
    coupa_build_receipt_from_response,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_purchase_order_from_response,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaPOReceiptComparisonResult:
    """Class to store the result of comparing a PO with a single receipt."""

    po_id: int
    receipt_id: int
    status: str
    message: str
    line_items_match: Dict[str, bool] = field(default_factory=dict)
    total_amount_match: bool = False
    total_amount_discrepancies: Dict[str, float] = field(default_factory=dict)
    quantity_match: Dict[str, bool] = field(default_factory=dict)
    unit_price_match: Dict[str, bool] = field(default_factory=dict)
    line_item_discrepancies: Dict[str, Dict[str, Dict[str, Union[str, float, None]]]] = field(
        default_factory=dict
    )
    currency_match: Dict[str, bool] = field(default_factory=dict)


@dataclass
class CoupaPOAllReceiptsComparisonResult:
    """Class to store the result of comparing a PO with all its receipts."""

    po_id: int
    status: str
    message: str
    receipt_comparisons: Dict[str, CoupaPOReceiptComparisonResult] = field(default_factory=dict)
    overall_status: str = "APPROVED"


@dataclass
class AggregatedReceiptData:
    """Helper class to store aggregated receipt data per order line."""

    quantity: float = 0.0
    total: float = 0.0
    prices: Set[float] = field(default_factory=set)
    currencies: Set[str] = field(default_factory=set)


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_po_all_receipts_matching(po_id: int) -> ToolResponse[CoupaPOAllReceiptsComparisonResult]:
    """
    Match a purchase order with all its corresponding receipts.

    Aggregates receipt data per order line and compares with the PO.

    Args:
        po_id: Purchase Order ID

    Returns:
        ToolResponse containing CoupaPOAllReceiptsComparisonResult with the results of comparison or error information.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure in retrieving credentials")

    po_response = client.get_request(resource_name=f"purchase_orders/{po_id}")
    if "errors" in po_response:
        return ToolResponse(
            success=False, message=coupa_format_error_string(po_response), content=None
        )

    if not po_response:
        result = CoupaPOAllReceiptsComparisonResult(
            po_id=po_id, status="error", message=f"PO {po_id} not found."
        )
        return ToolResponse(
            success=False, message=f"Purchase Order with ID {po_id} not found", content=result
        )

    po = coupa_build_purchase_order_from_response(po_response)
    if not po:
        result = CoupaPOAllReceiptsComparisonResult(
            po_id=po_id, status="error", message=f"PO {po_id} not found."
        )
        return ToolResponse(
            success=False,
            message=f"Failed to build purchase order from response for ID {po_id}",
            content=result,
        )

    params = {"order-line[order-header-id]": po_id, "fields": '["id"]'}
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
        result = CoupaPOAllReceiptsComparisonResult(
            po_id=po_id,
            status="BLOCKED",
            overall_status="BLOCKED",
            message=f"No receipts found for PO {po_id}",
        )
        return ToolResponse(
            success=False, message=f"No receipts found for PO {po_id}", content=result
        )

    aggregated_data: Dict[str, AggregatedReceiptData] = {}

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
                aggregated_data[key] = AggregatedReceiptData()

            aggregated_data[key].quantity += quantity_val
            aggregated_data[key].total += total_val
            aggregated_data[key].prices.add(price_val)
            if currency_code:
                aggregated_data[key].currencies.add(currency_code)

    po_lines = getattr(po, "order_lines", None)
    po_lines = getattr(po_lines, "order_lines", []) if po_lines else []

    status = "APPROVED"
    discrepancies_summary = []

    for po_line in po_lines:
        line_id = str(getattr(po_line, "order_line_id", ""))
        if line_id not in aggregated_data:
            status = "BLOCKED"
            discrepancies_summary.append(f"Missing receipts for order line {line_id}")
            continue

        agg = aggregated_data[line_id]
        line_type = getattr(po_line, "order_line_type", None)

        po_qty = float(getattr(po_line, "quantity", 0) or 0)
        po_price = float(getattr(po_line, "price", 0) or 0)
        po_total = float(getattr(po_line, "total", 0) or 0)
        po_currency = getattr(po, "currency", "")

        if line_type == "OrderQuantityLine":
            if abs(po_qty - agg.quantity) > 0.01:
                status = "BLOCKED"
                discrepancies_summary.append(f"Quantity mismatch on line {line_id}")
            if len(agg.prices) != 1 or abs(po_price - list(agg.prices)[0]) > 0.01:
                status = "BLOCKED"
                discrepancies_summary.append(f"Unit price mismatch on line {line_id}")
            if abs(po_total - agg.total) > 0.01:
                status = "BLOCKED"
                discrepancies_summary.append(f"Total amount mismatch on line {line_id}")
            if len(agg.currencies) != 1 or po_currency not in agg.currencies:
                status = "BLOCKED"
                discrepancies_summary.append(f"Currency mismatch on line {line_id}")
        elif line_type == "OrderAmountLine":
            if abs(po_total - agg.total) > 0.01:
                status = "BLOCKED"
                discrepancies_summary.append(f"Total amount mismatch on line {line_id}")
            if len(agg.currencies) != 1 or po_currency not in agg.currencies:
                status = "BLOCKED"
                discrepancies_summary.append(f"Currency mismatch on line {line_id}")
        else:
            status = "BLOCKED"
            discrepancies_summary.append(f"Unsupported line type on line {line_id}")

    message = (
        "All receipts match with PO" if status == "APPROVED" else "\n".join(discrepancies_summary)
    )

    result = CoupaPOAllReceiptsComparisonResult(
        po_id=po_id,
        status=status,
        overall_status=status,
        message=message,
    )

    return ToolResponse(
        success=True, message="PO-receipts matching completed successfully", content=result
    )
