from typing import Any, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaAddress,
    CoupaAddressList,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_helper_functions import (
    coupa_build_address,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_all_addresses(
    street1: Optional[str] = None,
    city: Optional[str] = None,
    postal_code: Optional[str] = None,
    state: Optional[str] = None,
    country_code: Optional[str] = None,
    country_name: Optional[str] = None,
    created_at_start: Optional[str] = None,
    created_at_end: Optional[str] = None,
    order_by_direction: Optional[str] = "desc",
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
) -> ToolResponse[CoupaAddressList]:
    """
    Retrieves addresses based on certain filter parameters.

    Args:
        street1: First street line of address (555 bailey ave).
        city: City of address (San Jose).
        postal_code: Postal code of address (95121).
        state: State/province of address (CA).
        country_code: 2 character code (US).
        country_name: Full country name: (India).
        created_at_start: The start of the date range for getting purchase orders (YYYY-MM-DD).
        created_at_end: The end of the date range for getting purchase orders (YYYY-MM-DD).
        order_by_direction: The direction in which the purchase orders will be ordered, ("asc" or
            "desc").
        limit: Optional, the count of purchase orders to return - default 10.
        offset: Optional, the number of entries to offset by for pagination - default 0.

    Returns:
        The resulting list of addresses.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    # order by created at time
    params: dict[str, Any] = {
        key: value
        for key, value in {
            "street1[contains]": street1,
            "city[contains]": city,
            "postal_code[contains]": postal_code,
            "state[contains]": state,
            "country[name][contains]": country_name,
            "country[code][contains]": country_code,
            "limit": limit,
            "offset": offset,
            "order_by": "created-at",
            "dir": order_by_direction,
            "created-at[gt]": created_at_start,
            "created-at[lt]": created_at_end,
        }.items()
        if value not in (None, "")
    }

    response = client.get_request_list(resource_name="addresses", params=params)
    if len(response) == 0:
        return ToolResponse(success=False, message="No addresses found.")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    address_list: List[CoupaAddress] = []
    for entry in response:
        address = coupa_build_address(entry)
        address_list.append(address)

    return ToolResponse(
        success=True,
        message="Addresses retrieved successfully.",
        content=CoupaAddressList(address_list=address_list),
    )
