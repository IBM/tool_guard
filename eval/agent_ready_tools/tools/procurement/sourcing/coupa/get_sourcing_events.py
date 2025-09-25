from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaQuoteRequest:
    """responses in quote request."""

    event_id: int
    event_name: Optional[str]
    event_type: str
    state: str
    start_date: Optional[str]
    end_date: Optional[str]
    created_at: str


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_sourcing_events(
    event_type: str = "rfp",
    event_name: Optional[str] = None,
    state: Optional[str] = None,
    creator: Optional[str] = None,
    creation_date: Optional[str] = None,
    item: Optional[str] = None,
    start_date: Optional[str] = None,
) -> ToolResponse[List[CoupaQuoteRequest]]:
    """
    Get sourcing events created from requisition.

    Args:
        event_type: Type of event, Defaults to rfp.
        event_name: The name of the event. Defaults to None.
        state: Filters events based on their status, Defaults to None.
        creator: The name of the event creator. Defaults to None.
        creation_date: The date when the event was created in ISO 8601 format. Filters events
            created from this date. Defaults to None.
        item: Filters events based on item details. Defaults to None.
        start_date: The date when the event starts in ISO 8601 format. Filters events starting from
            this date. Defaults to None.

    Returns:
        List of sourcing events of type rfp
    """
    params = {
        "event-type": event_type,
        "fields": '["id","description","created-at","start-time","state","end-time","event-type"]',
        "description": event_name,
        "state": state,
        "created-by[fullname][starts_with]": creator,
        "created-at[gt_or_eq]": creation_date,
        "lines[description]": item,
        "start-time[gt_or_eq]": start_date,
    }

    params = {key: value for key, value in params.items() if value}
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.get_request_list(resource_name="quote_requests", params=params)

    if len(response) == 1 and "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    if len(response) == 0:
        return ToolResponse(
            success=True, message="No sourcing events were found based on the provided criteria."
        )

    resource_quote = []
    for r in response:
        resource_quote.append(
            CoupaQuoteRequest(
                event_id=r.get("id", 0),
                event_name=r.get("description", ""),
                event_type=r.get("event-type", ""),
                state=r.get("state", ""),
                start_date=r.get("start-time", ""),
                end_date=r.get("end-time", ""),
                created_at=r.get("created-at", ""),
            )
        )
    return ToolResponse(
        success=True,
        message="The sourcing events were successfully retrieved",
        content=resource_quote,
    )
