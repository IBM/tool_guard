from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAccountType,
    CoupaGetAccountTypesResponse,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_account_types() -> ToolResponse[CoupaGetAccountTypesResponse]:
    """
    returns a list of all account types (chart of accounts) that can be used for billing a line
    item.

    Returns:
        All of the account types
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {
        "active": True,
        "fields": '["id","name","active",{"currency": ["code"]}]',
    }

    response = client.get_request_list(resource_name="account_types", params=params)
    if len(response) == 0:
        return ToolResponse(success=False, message="No account types found.")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    return ToolResponse(
        success=True,
        message="Account types retrieved successfully.",
        content=CoupaGetAccountTypesResponse(
            total_count=len(response),
            account_types=[
                CoupaAccountType(
                    account_type_id=int(r.get("id", 0)),
                    account_type_name=r.get("name", ""),
                    active=r.get("active", False),
                    currency_code=r.get("currency", {}).get("code", "USD"),
                )
                for r in response
            ],
        ),
    )
