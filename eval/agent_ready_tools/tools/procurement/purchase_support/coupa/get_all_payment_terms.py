from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaPaymentTerms,
    CoupaPaymentTermsList,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_all_payment_terms() -> ToolResponse[CoupaPaymentTermsList]:
    """
    Retrieves the all payment terms in Coupa.

    Returns:
        The retrieved list of payment terms in this Coupa instance.
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request_list(resource_name="payment_terms")
    if len(response) == 0:
        return ToolResponse(success=False, message="No payment terms found.")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    payment_terms_list: List[CoupaPaymentTerms] = []

    for payment_term in response:
        payment_terms_list.append(
            CoupaPaymentTerms(
                payment_id=payment_term["id"],
                payment_code=payment_term["code"],
                payment_active_status=payment_term["active"],
            )
        )

    return ToolResponse(
        success=True,
        message="Payment terms retrieved successfully.",
        content=CoupaPaymentTermsList(payment_terms_list=payment_terms_list),
    )
