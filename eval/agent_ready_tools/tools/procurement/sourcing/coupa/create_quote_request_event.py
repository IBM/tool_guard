from typing import Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.sourcing.coupa.common_classes_sourcing import LinesType
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils import format_tool_input
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CreateRFP:
    """Represents the creation of the Request Of Purchase in the Coupa."""

    event_name: str
    event_id: int
    state: str


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_create_quote_request_event(
    event_name: str,
    commodity_name: str,
    line_type: str,
    supplier_name: str,
    supplier_email: str,
    quantity: str,
    price_amount: str,
    item: Optional[str] = None,
) -> ToolResponse[CreateRFP]:
    """
    Create rfp event in Coupa.

    Args:
        event_name: The event name in the Coupa.
        commodity_name: The commodity name of the event in the coupa returned by `get_commodities`
            tool.
        line_type: The line type of item in the Coupa.
        supplier_name: The supplier name in the Coupa returned by `get_supplier` tool.
        supplier_email: The supplier email in the coupa returned by `get_supplier` tool.
        quantity: The quantity of the item in the Coupa.
        price_amount: The price amount of the item in the Coupa.
        item: The item name in the coupa returned by `search_item_by_name` tool.

    Returns:
        Result from creating a rfp event.
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    suppliers_names: List[str] = (
        format_tool_input.string_to_list_of_strings(supplier_name)
        if isinstance(supplier_name, str)
        else supplier_name
    )
    suppliers_emails: List[str] = (
        format_tool_input.string_to_list_of_strings(supplier_email)
        if isinstance(supplier_email, str)
        else supplier_email
    )

    suppliers_details: List[Dict[str, str]] = [
        {"name": name, "email": email} for name, email in zip(suppliers_names, suppliers_emails)
    ]

    payload = {
        "event-type": "rfp",
        "description": event_name,
        "lines": [
            {
                "type": LinesType[line_type.strip().upper()].value,
                "quantity": quantity,
                "price-amount": price_amount,
                "description": item,
            }
        ],
        "quote-suppliers": suppliers_details,
        "commodity": {"name": commodity_name},
    }
    response = client.post_request(resource_name="quote_requests", payload=payload)

    if "errors" in response:
        return ToolResponse(
            success=False, message=coupa_format_error_string(response), content=None
        )

    return ToolResponse(
        success=True,
        message="The quote request was successfully created",
        content=CreateRFP(
            event_name=response.get("description", ""),
            event_id=response.get("id", 0),
            state=response.get("state", ""),
        ),
    )
