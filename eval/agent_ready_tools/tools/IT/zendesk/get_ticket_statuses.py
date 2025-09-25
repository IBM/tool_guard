from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class TicketStatus:
    """Represents a ticket status in Zendesk."""

    id: int
    name: str


@dataclass
class GetTicketStatusesResponse:
    """Response containing all ticket statuses from Zendesk."""

    ticket_statuses: List[TicketStatus]
    error_description: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def get_ticket_statuses(status: Optional[str] = None) -> GetTicketStatusesResponse:
    """
    Retrieves all ticket statuses from Zendesk.

    Args:
        status: The name of the ticket status to filter.

    Returns:
        A list of ticket statuses.
    """
    try:
        client = get_zendesk_client()

        # Optional filter
        params = {"status_categories": status} if status else None
        response = client.get_request(entity="custom_statuses", params=params)

        ticket_statuses = [
            TicketStatus(id=status.get("id"), name=status.get("agent_label", ""))
            for status in response.get("custom_statuses", [])
        ]

        return GetTicketStatusesResponse(ticket_statuses=ticket_statuses)

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else {}
        error_description = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )

        return GetTicketStatusesResponse(
            ticket_statuses=[],
            error_description=error_description,
            http_code=e.response.status_code if e.response else 500,
        )

    except Exception as e:  # pylint: disable=broad-except
        return GetTicketStatusesResponse(
            ticket_statuses=[],
            http_code=500,
            error_description=str(e),
        )
