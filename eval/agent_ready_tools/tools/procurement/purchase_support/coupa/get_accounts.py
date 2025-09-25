from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAccount,
    CoupaGetAccountsResponse,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_accounts(
    account_type_id: int = 1, offset: int = 0
) -> ToolResponse[CoupaGetAccountsResponse]:
    """
    returns a list of all accounts under a certain chart of accounts.

    Args:
        account_type_id: chart of accounts
        offset: value to offset search results by for pagination

    Returns:
        All of the accounts
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {
        "active": True,
        "account-type-id": account_type_id,
        "fields": '["id", "name", "code", "active", "account-type-id"]',
        "limit": 10,
        "offset": offset,
    }

    response = client.get_request_list(resource_name="accounts", params=params)
    if len(response) == 0:
        return ToolResponse(success=False, message="No accounts found.")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    return ToolResponse(
        success=True,
        message="Accounts retrieved successfully.",
        content=CoupaGetAccountsResponse(
            total_count=len(response),
            accounts=[
                CoupaAccount(
                    account_id=int(r.get("id", 0)),
                    account_name=r.get("name", ""),
                    account_code=r.get("code", ""),
                    active=r.get("active", None),
                    account_type_id=r.get("account-type-id", None),
                )
                for r in response
            ],
        ),
    )
