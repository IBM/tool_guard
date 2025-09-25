from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaShippingTerms,
    CoupaShippingTermsList,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_shipping_terms() -> ToolResponse[CoupaShippingTermsList]:
    """
    Retrieve the shipping terms in Coupa.

    Returns:
        The retrieved list of shipping terms in this coupa instance
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"active": True}

    response = client.get_request_list(resource_name="shipping_terms", params=params)
    if len(response) == 0:
        return ToolResponse(success=False, message="No addresses found.")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    shipping_terms_list: List[CoupaShippingTerms] = []
    for shipping_term in response:
        shipping_terms_list.append(
            CoupaShippingTerms(
                shipping_id=shipping_term["id"],
                shipping_code=shipping_term["code"],
                active_status=shipping_term["active"],
            )
        )
    return ToolResponse(
        success=True,
        message="Shipping terms retrieved successfully.",
        content=CoupaShippingTermsList(shipping_terms_list=shipping_terms_list),
    )
