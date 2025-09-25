"""This module provides functionality for 3-way matching between invoices, purchase orders, and
receipts."""

from dataclasses import field
from typing import Annotated, Any, Dict, Optional, Set

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import ValidationError
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.invoice_management.coupa.helper_functions_invoice_management import (
    coupa_build_invoice_from_response,
    coupa_build_receipt_from_response,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_purchase_order_from_response,
)
from agent_ready_tools.utils.format_tool_input import string_to_list_of_ints
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class UnitPriceComparison:
    """Helper class to store simple unit price comparison results."""

    invoice_price: float = 0.0
    po_price: float = 0.0
    receipt_prices: Set[float] = field(default_factory=set)
    average_receipt_price: float = 0.0


def compare_unit_prices(
    invoice_price: float,
    po_price: float,
    receipt_prices: Set[float],
) -> UnitPriceComparison:
    """Perform simple unit price comparison."""
    comparison = UnitPriceComparison(
        invoice_price=invoice_price,
        po_price=po_price,
        receipt_prices=receipt_prices,
        average_receipt_price=(
            (sum(receipt_prices) / len(receipt_prices)) if receipt_prices else 0.0
        ),
    )
    return comparison


@dataclass
class ThreeWayComparisonResult:
    """Dataclass to store the results of 3-way comparison between Invoice, PO, and Receipts."""

    invoice_id: int
    po_id: int
    overall_status: str
    message: str

    invoice_po_status: str = "APPROVED"
    invoice_po_message: str = ""
    invoice_po_line_matches: Dict[str, bool] = field(default_factory=dict)
    invoice_po_discrepancies: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    invoice_receipts_status: str = "APPROVED"
    invoice_receipts_message: str = ""
    invoice_receipts_line_matches: Dict[str, bool] = field(default_factory=dict)
    invoice_receipts_discrepancies: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    po_receipts_status: str = "APPROVED"
    po_receipts_message: str = ""
    po_receipts_line_matches: Dict[str, bool] = field(default_factory=dict)
    po_receipts_discrepancies: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    total_amounts: Dict[str, float] = field(default_factory=dict)
    currency_matches: Dict[str, bool] = field(default_factory=dict)

    unit_price_comparisons: Dict[str, UnitPriceComparison] = field(default_factory=dict)


@dataclass
class AggregatedReceiptData:
    """Helper class to store aggregated receipt data per order line."""

    quantity: float = 0.0
    total: float = 0.0
    prices: Set[float] = field(default_factory=set)
    currencies: Set[str] = field(default_factory=set)
    descriptions: Set[str] = field(default_factory=set)


@dataclass
class BatchThreeWayComparisonResult:
    """Dataclass to store the results of batch 3-way comparison for multiple invoices."""

    total_invoices: int
    successful_matches: int
    blocked_matches: int
    error_matches: int
    results: list[ThreeWayComparisonResult] = field(default_factory=list)
    summary: str = ""


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_batch_three_way_matching(
    invoice_ids: Annotated[list[int], string_to_list_of_ints],
) -> ToolResponse[BatchThreeWayComparisonResult]:
    """
    Perform 3-way matching for a list of invoices, their purchase orders, and receipts.

    This tool processes multiple invoices in batch and provides a summary of results.

    Args:
        invoice_ids: List of invoice IDs to analyze

    Returns:
        BatchThreeWayComparisonResult containing results for all invoices
    """

    batch_result = BatchThreeWayComparisonResult(
        total_invoices=len(invoice_ids),
        successful_matches=0,
        blocked_matches=0,
        error_matches=0,
        results=[],
        summary="",
    )

    for invoice_id in invoice_ids:
        try:
            result = coupa_three_way_matching(invoice_id)
            batch_result.results.append(result)

            if result.overall_status == "APPROVED":
                batch_result.successful_matches += 1
            elif result.overall_status == "BLOCKED":
                batch_result.blocked_matches += 1
            elif result.overall_status == "error":
                batch_result.error_matches += 1

        except BaseException as e:
            error_result = ThreeWayComparisonResult(
                invoice_id=invoice_id,
                po_id=0,
                overall_status="error",
                message=f"Unexpected error processing invoice {invoice_id}: {str(e)}",
            )
            batch_result.results.append(error_result)
            batch_result.error_matches += 1

    batch_result.summary = (
        f"Processed {batch_result.total_invoices} invoices: "
        f"{batch_result.successful_matches} approved, "
        f"{batch_result.blocked_matches} blocked, "
        f"{batch_result.error_matches} errors"
    )

    return ToolResponse(
        success=True,
        message=batch_result.summary,
        content=batch_result,
    )


def coupa_three_way_matching(invoice_id: int) -> ThreeWayComparisonResult:
    """
    Perform 3-way matching between an invoice, its purchase order, and all receipts.

    This tool combines the logic from:
    - Invoice vs PO matching
    - Invoice vs Receipts matching
    - PO vs Receipts matching

    Args:
        invoice_id: The ID of the invoice to analyze

    Returns:
        ThreeWayComparisonResult containing comprehensive comparison results
    """

    client = get_coupa_client()

    invoice_response = client.get_request(resource_name=f"invoices/{invoice_id}")

    if not invoice_response:
        return ThreeWayComparisonResult(
            invoice_id=invoice_id,
            po_id=0,
            overall_status="error",
            message=f"Invoice with ID {invoice_id} not found.",
        )

    invoice = coupa_build_invoice_from_response(invoice_response)

    if not invoice:
        return ThreeWayComparisonResult(
            invoice_id=invoice_id,
            po_id=0,
            overall_status="error",
            message=f"Invoice with ID {invoice_id} not found.",
        )

    # Extract PO number from invoice
    po_number = next(
        (line.po_number for line in invoice.invoice_lines if line and line.po_number), None
    )

    po_number_int = 0
    if po_number is not None:
        try:
            po_number_int = int(po_number)
        except (ValueError, TypeError):
            po_number_int = 0

    if not po_number:
        return ThreeWayComparisonResult(
            invoice_id=invoice_id,
            po_id=po_number_int,
            overall_status="error",
            message="Purchase Order not found in invoice lines.",
        )

    po_response = client.get_request(resource_name=f"purchase_orders/{po_number}")
    po = coupa_build_purchase_order_from_response(po_response)

    if not po:
        return ThreeWayComparisonResult(
            invoice_id=invoice_id,
            po_id=po_number_int,
            overall_status="error",
            message=f"Purchase Order with ID {po_number} not found.",
        )

    params = {"order-line[order-header-id]": po_number, "fields": '["id"]'}
    receipt_response = client.get_request_list(
        resource_name="receiving_transactions", params=params
    )
    receipt_ids = [
        item.get("id")
        for item in receipt_response
        if isinstance(item, dict) and "id" in item and isinstance(item.get("id"), int)
    ]

    if not receipt_ids:
        return ThreeWayComparisonResult(
            invoice_id=invoice_id,
            po_id=po_number_int,
            overall_status="BLOCKED",
            message=f"No receipts found for PO {po_number}",
            invoice_po_status="APPROVED",
            invoice_receipts_status="BLOCKED",
            po_receipts_status="BLOCKED",
        )

    try:
        result = ThreeWayComparisonResult(
            invoice_id=invoice_id,
            po_id=po_number_int,
            overall_status="APPROVED",
            message="All 3-way matches are successful",
        )

        invoice_currency = invoice.currency.code if invoice.currency else ""
        po_currency = po.currency if po.currency else ""

        aggregated_data: Dict[str, AggregatedReceiptData] = {}

        for receipt_id in receipt_ids:
            response = client.get_request(resource_name=f"receiving_transactions/{receipt_id}")
            receipt = coupa_build_receipt_from_response(response)

            if receipt.status == "voided":
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

                    if (
                        hasattr(item, "account")
                        and item.account
                        and item.account.account_type
                        and item.account.account_type.currency
                    ):
                        currency_code = item.account.account_type.currency.code
                    elif (
                        hasattr(receipt, "account")
                        and receipt.account
                        and receipt.account.account_type
                        and receipt.account.account_type.currency
                    ):
                        currency_code = receipt.account.account_type.currency.code
                except AttributeError:
                    pass

                if key not in aggregated_data:
                    aggregated_data[key] = AggregatedReceiptData()

                aggregated_data[key].quantity += quantity_val
                aggregated_data[key].total += total_val
                aggregated_data[key].prices.add(price_val)
                if currency_code:
                    aggregated_data[key].currencies.add(currency_code)

                description = (
                    order_line.get("description", "").strip()
                    if isinstance(order_line, dict)
                    else ""
                )
                if description:
                    aggregated_data[key].descriptions.add(description)

        invoice_total = 0.0
        po_total = 0.0
        receipts_total = 0.0

        invoice_lines = invoice.invoice_lines
        po_lines = po.order_lines.order_lines

        po_lines_dict = {line.order_line_id: line for line in po_lines}
        invoice_lines_dict = {line.order_line_id: line for line in invoice_lines}

        for line_num, invoice_line in invoice_lines_dict.items():
            po_line = po_lines_dict.get(line_num or -1)
            line_id = str(line_num)

            result.invoice_po_line_matches[line_id] = True
            result.invoice_receipts_line_matches[line_id] = True
            result.po_receipts_line_matches[line_id] = True

            result.invoice_po_discrepancies[line_id] = {}
            result.invoice_receipts_discrepancies[line_id] = {}
            result.po_receipts_discrepancies[line_id] = {}

            # INVOICE vs PO COMPARISON
            if po_line:

                invoice_quantity = float(invoice_line.quantity or 0)
                po_quantity = float(po_line.quantity or 0)
                if invoice_quantity != po_quantity:
                    result.invoice_po_line_matches[line_id] = False
                    result.invoice_po_discrepancies[line_id]["quantity"] = {
                        "invoice": invoice_quantity,
                        "po": po_quantity,
                    }

                invoice_price = float(invoice_line.price or 0)
                po_price = float(po_line.price or 0)
                receipt_prices = aggregated_data.get(line_id, AggregatedReceiptData()).prices

                price_comparison = compare_unit_prices(
                    invoice_price=invoice_price, po_price=po_price, receipt_prices=receipt_prices
                )

                result.unit_price_comparisons[line_id] = price_comparison

                if invoice_price != po_price:
                    result.invoice_po_line_matches[line_id] = False
                    result.invoice_po_discrepancies[line_id]["unit_price"] = {
                        "invoice": invoice_price,
                        "po": po_price,
                    }

                invoice_line_total = float(invoice_line.total or 0)
                po_line_total = float(po_line.total or 0)
                if invoice_line_total != po_line_total:
                    result.invoice_po_line_matches[line_id] = False
                    result.invoice_po_discrepancies[line_id]["line_total"] = {
                        "invoice": invoice_line_total,
                        "po": po_line_total,
                    }

                if invoice_currency != po_currency:
                    result.invoice_po_line_matches[line_id] = False
                    result.invoice_po_discrepancies[line_id]["currency"] = {
                        "invoice": invoice_currency,
                        "po": po_currency,
                    }

                po_total += po_line_total
            else:
                result.invoice_po_line_matches[line_id] = False
                result.invoice_po_discrepancies[line_id]["error"] = "Line item not found in PO"

            # INVOICE vs RECEIPTS COMPARISON
            if line_id in aggregated_data:
                agg = aggregated_data[line_id]
                invoice_total += float(invoice_line.total or 0)
                receipts_total += agg.total

                invoice_quantity = float(invoice_line.quantity or 0.0)
                if abs(invoice_quantity - agg.quantity) > 0.01:
                    result.invoice_receipts_line_matches[line_id] = False
                    result.invoice_receipts_discrepancies[line_id]["quantity"] = {
                        "invoice": invoice_quantity,
                        "receipts": agg.quantity,
                    }

                invoice_price = float(invoice_line.price or 0.0)
                if (
                    invoice_price != price_comparison.average_receipt_price
                ):  # Compare to average receipt price
                    result.invoice_receipts_line_matches[line_id] = False
                    result.invoice_receipts_discrepancies[line_id]["unit_price"] = {
                        "invoice": invoice_price,
                        "receipts": list(agg.prices),
                        "average_receipt_price": price_comparison.average_receipt_price,
                    }

                if len(agg.currencies) > 1 or (
                    invoice_currency and invoice_currency not in agg.currencies
                ):
                    result.invoice_receipts_line_matches[line_id] = False
                    result.invoice_receipts_discrepancies[line_id]["currency"] = {
                        "invoice": invoice_currency,
                        "receipts": list(agg.currencies),
                    }
            else:
                result.invoice_receipts_line_matches[line_id] = False
                result.invoice_receipts_discrepancies[line_id]["error"] = {
                    "message": "No matching receipts"
                }

            # PO vs RECEIPTS COMPARISON
            if po_line and line_id in aggregated_data:
                agg = aggregated_data[line_id]
                line_type = getattr(po_line, "order_line_type", None)

                po_qty = float(getattr(po_line, "quantity", 0) or 0)
                po_price = float(getattr(po_line, "price", 0) or 0)
                po_line_total = float(getattr(po_line, "total", 0) or 0)

                if line_type == "OrderQuantityLine":
                    if abs(po_qty - agg.quantity) > 0.01:
                        result.po_receipts_line_matches[line_id] = False
                        result.po_receipts_discrepancies[line_id]["quantity"] = {
                            "po": po_qty,
                            "receipts": agg.quantity,
                        }

                    if po_price != price_comparison.average_receipt_price:
                        result.po_receipts_line_matches[line_id] = False
                        result.po_receipts_discrepancies[line_id]["unit_price"] = {
                            "po": po_price,
                            "receipts": list(agg.prices),
                            "average_receipt_price": price_comparison.average_receipt_price,
                        }

                    if abs(po_line_total - agg.total) > 0.01:
                        result.po_receipts_line_matches[line_id] = False
                        result.po_receipts_discrepancies[line_id]["line_total"] = {
                            "po": po_line_total,
                            "receipts": agg.total,
                        }

                    if len(agg.currencies) != 1 or po_currency not in agg.currencies:
                        result.po_receipts_line_matches[line_id] = False
                        result.po_receipts_discrepancies[line_id]["currency"] = {
                            "po": po_currency,
                            "receipts": list(agg.currencies),
                        }
                elif line_type == "OrderAmountLine":
                    if abs(po_line_total - agg.total) > 0.01:
                        result.po_receipts_line_matches[line_id] = False
                        result.po_receipts_discrepancies[line_id]["line_total"] = {
                            "po": po_line_total,
                            "receipts": agg.total,
                        }

                    if len(agg.currencies) != 1 or po_currency not in agg.currencies:
                        result.po_receipts_line_matches[line_id] = False
                        result.po_receipts_discrepancies[line_id]["currency"] = {
                            "po": po_currency,
                            "receipts": list(agg.currencies),
                        }
            elif po_line:
                result.po_receipts_line_matches[line_id] = False
                result.po_receipts_discrepancies[line_id]["error"] = "No matching receipts"

        if not all(result.invoice_po_line_matches.values()):
            result.invoice_po_status = "BLOCKED"
            result.invoice_po_message = "Discrepancies found between invoice and PO"

        if not all(result.invoice_receipts_line_matches.values()):
            result.invoice_receipts_status = "BLOCKED"
            result.invoice_receipts_message = "Discrepancies found between invoice and receipts"

        if not all(result.po_receipts_line_matches.values()):
            result.po_receipts_status = "BLOCKED"
            result.po_receipts_message = "Discrepancies found between PO and receipts"

        po_total_with_tax = float(po.total_with_estimated_tax or 0)
        invoice_total_with_tax = float(invoice.total_with_taxes or 0)

        result.total_amounts = {
            "invoice": invoice_total_with_tax,
            "po": po_total_with_tax,
            "receipts": receipts_total,
        }

        if (
            result.invoice_po_status == "BLOCKED"
            or result.invoice_receipts_status == "BLOCKED"
            or result.po_receipts_status == "BLOCKED"
        ):
            result.overall_status = "BLOCKED"
            result.message = "3-way matching failed - discrepancies found"
        else:
            result.overall_status = "APPROVED"
            result.message = "All 3-way matches are successful"

        if result.invoice_po_status == "APPROVED":
            result.invoice_po_message = "Invoice and PO match successfully"
        if result.invoice_receipts_status == "APPROVED":
            result.invoice_receipts_message = "Invoice and receipts match successfully"
        if result.po_receipts_status == "APPROVED":
            result.po_receipts_message = "PO and receipts match successfully"

        # Convert all set fields to lists for JSON serialization

        for disc in result.invoice_receipts_discrepancies.values():
            if "unit_price" in disc and isinstance(disc["unit_price"].get("receipts"), set):
                disc["unit_price"]["receipts"] = list(disc["unit_price"]["receipts"])
            if "currency" in disc and isinstance(disc["currency"].get("receipts"), set):
                disc["currency"]["receipts"] = list(disc["currency"]["receipts"])

        for disc in result.po_receipts_discrepancies.values():
            if "unit_price" in disc and isinstance(disc["unit_price"].get("receipts"), set):
                disc["unit_price"]["receipts"] = list(disc["unit_price"]["receipts"])
            if "currency" in disc and isinstance(disc["currency"].get("receipts"), set):
                disc["currency"]["receipts"] = list(disc["currency"]["receipts"])

        return result

    except ValidationError as e:
        return ThreeWayComparisonResult(
            invoice_id=invoice_id,
            po_id=po_number_int,
            overall_status="error",
            message=f"Error during 3-way matching: {e}",
        )
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        return ThreeWayComparisonResult(
            invoice_id=invoice_id,
            po_id=po_number_int,
            overall_status="error",
            message=f"Error comparing documents: {str(e)}",
        )
