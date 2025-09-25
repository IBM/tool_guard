from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CoupaSupplierDetails,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_all_suppliers(
    status: Optional[str] = None,
    number: Optional[str] = None,
    name: Optional[str] = None,
    limit: int = 10,
    skip: int = 0,
) -> ToolResponse[List[CoupaSupplierDetails]]:
    """
    Get all suppliers from Coupa.

    Args:
        status: A status filter, defaults to None
        number: A supplier number filter
        name: A supplier name filter
        limit: number of suppliers returned
        skip: number of suppliers to skip for pagination

    Returns:
        A list of suppliers
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {
        "fields": '["id","number","status","name",{"primary_contact":["email"]}]',
        "status": status,
        "name[contains]": name,
        "number": number,
        "limit": limit,
        "offset": skip,
    }

    params = {key: value for key, value in params.items() if value is not None}

    response = client.get_request_list(
        resource_name="suppliers",
        params=params,
    )

    if len(response) == 0:
        return ToolResponse(success=False, message="No suppliers returned")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    suppliers = []
    for supplier in response:
        suppliers.append(
            CoupaSupplierDetails(
                id=supplier["id"],
                number=supplier["number"],
                status=supplier["status"],
                name=supplier["name"],
                contact_email=supplier["primary-contact"]["email"],
            )
        )

    return ToolResponse(success=True, message="Get all suppliers successful", content=suppliers)
