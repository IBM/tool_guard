from typing import Any, Dict, List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_create_an_invoice(
    po_id: int,
    invoice_number: str,
    invoice_date_str: str,
    shipping_amount: float = 0.0,
    handling_amount: float = 0.0,
    misc_amount: float = 0.0,
) -> ToolResponse[int]:
    """
    create an invoice against a purchase order.

    Args:
        po_id: purchase order id in which a new invoice is based
        invoice_number: an invoice number
        invoice_date_str: invoice date in string format
        shipping_amount: shipping_amount
        handling_amount: handling_amount
        misc_amount: misc_amount

    Returns:
        ID of the resulting new invoice
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    resource_name_po = f"purchase_orders/{po_id}"
    po = client.get_request(resource_name=resource_name_po)
    if "errors" in po:
        return ToolResponse(success=False, message=coupa_format_error_string(po))
    currency_code = po.get("currency", {}).get("code", "USD")  # USD is the default currency code
    supplier_id = po.get("supplier", {}).get("id", 0)
    po_order_lines = po.get("order-lines", [])

    if not isinstance(po_order_lines, list) or len(po_order_lines) == 0:
        return ToolResponse(
            success=False,
            message="At least 1 order line in the purchase order is required for creating the invoie.",
        )

    invoice_lines: List[Dict[str, Any]] = []
    sum_total_with_estimated_tax = 0.0
    sum_estimated_tax_amount = 0.0
    sum_total = 0.0
    for order_line in po_order_lines:
        estimated_tax_amount = float(order_line.get("estimated-tax-amount", "0.00"))
        total_with_estimated_tax = float(order_line.get("total-with-estimated-tax", "0.00"))
        total = float(order_line.get("total", "0.00"))
        invoice_line = {
            "order-line-id": order_line.get("id", 0),
            "type": (
                "InvoiceQuantityLine"
                if order_line.get("type", "") == "OrderQuantityLine"
                else "InvoiceAmountLine"
            ),
            "price": order_line.get("price"),
            "quantity": order_line.get("quantity"),
            "total": order_line.get("total"),
            "uom": {
                "code": order_line.get("uom", {}).get("code"),
            },
            "description": order_line.get("description", ""),
            "account": {
                "id": order_line.get("account", {}).get("id", 0),
                "account-type-id": order_line.get("account", {}).get("account-type-id", 0),
            },
        }
        invoice_lines.append(invoice_line)
        if estimated_tax_amount:
            sum_estimated_tax_amount += float(estimated_tax_amount)
        if total_with_estimated_tax:
            sum_total_with_estimated_tax += float(total_with_estimated_tax)
        sum_total += float(total)

    if sum_total == 0:
        return ToolResponse(success=False, message="The sum total is equal to zero.")

    if sum_total_with_estimated_tax != float(po.get("total-with-estimated-tax", "0.00")):
        return ToolResponse(
            success=False, message="The total with tax does not match the purchase order sum total."
        )

    if sum_estimated_tax_amount != float(po.get("estimated-tax-amount", "0.00")):
        return ToolResponse(
            success=False, message="The estimated tax amount does not match the purchase order."
        )

    gross_total = float(sum_total) + shipping_amount + handling_amount + misc_amount
    invoice_data: Dict[str, Any] = {
        "supplier": {
            "id": supplier_id,
        },
        "invoice-number": invoice_number,
        "invoice-date": invoice_date_str,
        "currency": {
            "code": currency_code,
        },
        "invoice-lines": invoice_lines,
        "shipping-amount": f"{shipping_amount}",
        "handling-amount": f"{handling_amount}",
        "misc-amount": f"{misc_amount}",
        "tax-amount": f"{po.get('estimated-tax-amount', '0.00')}",
        "total-with-taxes": f"{po.get('total-with-estimated-tax', '0.00')}",
        "gross-total": f"{gross_total}",
    }
    resource_name_invoice = "invoices"
    response = client.post_request(resource_name=resource_name_invoice, payload=invoice_data)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    new_invoice_id = response.get("id")

    return ToolResponse(
        success=True,
        message=f"The invoice ID {new_invoice_id} was successfully created.",
        content=new_invoice_id,
    )
