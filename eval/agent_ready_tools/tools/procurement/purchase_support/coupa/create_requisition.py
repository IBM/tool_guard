from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaCreateRequisitionResponse,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_create_requisition(
    requester_login_name: str,
    currency_code: str = "USD",
) -> ToolResponse[CoupaCreateRequisitionResponse]:
    """
    Creates an empty requisition for a requesting user in Coupa.

    Args:
        requester_login_name: The requester's login name uniquely identifying them within the Coupa
            deployment.
        currency_code: The currency code.

    Returns:
        The result from submitting the requisition creation request.
    """
    try:
        client = get_coupa_client(scope=["core.requisition.read", "core.requisition.write"])
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload = {
        "requested-by": {"login": f"{requester_login_name}"},
        "currency": {"code": currency_code},
    }

    response = client.post_request(resource_name="requisitions/create_as_cart", payload=payload)
    if "errors" in response:
        return ToolResponse(success=False, message=coupa_format_error_string(response))

    return ToolResponse(
        success=True,
        message="Requisition was successfully created.",
        content=CoupaCreateRequisitionResponse(requisition_id=response["id"]),
    )
