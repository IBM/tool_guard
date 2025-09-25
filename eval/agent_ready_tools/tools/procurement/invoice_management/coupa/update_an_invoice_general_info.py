from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_an_invoice_general_info(
    invoice_id: int,
    invoice_number: Optional[str] = None,
    invoice_date: Optional[str] = None,
    currency_code: Optional[str] = None,
    shipping_amount: Optional[str] = None,
    handling_amount: Optional[str] = None,
    misc_amount: Optional[str] = None,
    paid: Optional[bool] = None,
    payment_date: Optional[str] = None,
    payment_notes: Optional[str] = None,
) -> ToolResponse[bool]:
    """
    Update payment information of an invoice.

    Args:
        invoice_id: a unique invoice identifier
        invoice_number: invoice number
        invoice_date: invoice date
        currency_code: currency code
        shipping_amount: shipping amount
        handling_amount: handling amount
        misc_amount: miscellaneous amount
        paid: whether a payment was made or not
        payment_date: payment date
        payment_notes: payment notes

    Returns:
        True if updated sucessfully. False otherwise.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params: Dict[str, Any] = {
        "invoice-number": invoice_number,
        "invoice-date": invoice_date,
        "shipping-amount": shipping_amount,
        "handling-amount": handling_amount,
        "misc-amount": misc_amount,
        "paid": paid,
        "payment-date": payment_date,
        "payment-notes": payment_notes,
    }
    data: Dict[str, Any] = {key: val for key, val in params.items() if val is not None}
    if currency_code is not None:
        data["currency"] = {}
        data["currency"]["code"] = currency_code
    resource_name = f"invoices/{invoice_id}"
    response = client.put_request(resource_name=resource_name, payload=data)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(success=True, message="The invoice was successfully updated.", content=True)
