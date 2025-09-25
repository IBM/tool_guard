from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_utility import (
    get_custom_field_key_id,
    get_name_by_id,
)
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class Ticket:
    """Represents a ticket in Zendesk."""

    ticket_id: str
    subject: str
    created_at: str
    description: Optional[str] = None
    status: Optional[str] = None
    assignee_name: Optional[str] = None
    submitter_name: Optional[str] = None
    requester_name: Optional[str] = None
    organization_name: Optional[str] = None
    group_name: Optional[str] = None
    priority: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


@dataclass
class GetTicketsResponse:
    """Represents the response for retrieving tickets in Zendesk."""

    tickets: List[Ticket]
    page: Optional[int]
    per_page: Optional[int]
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def zendesk_get_tickets(
    search: Optional[str] = None, per_page: Optional[int] = 10, page: Optional[int] = 1
) -> GetTicketsResponse:
    """
    Gets tickets from Zendesk.

    Args:
        search: Optional search query. This is how users can use search: Search for a specific word (e.g., Greenbriar), search for an exact string (e.g., "Greenbriar Corporation"), search for a ticket by id (e.g., 3245227), search for a resource type (e.g., "Jane Doe"), search by ticket status (e.g., status:open), search by date (e.g., created<2099-05-01).
        per_page: Number of tickets to retrieve per page. Defaults to 10.
        page: Page number to retrieve. Defaults to 1.

    Returns:
        List of tickets and their details.
    """
    try:
        client = get_zendesk_client()

        # Fetch ticket fields
        ticket_fields_response = client.get_request(entity="ticket_fields")

        # Extract the custom field names from the response
        custom_field_name = ticket_fields_response.get("ticket_fields", [])

        query = "type:ticket " + search if search else "type:ticket"
        params = {
            "query": query,
            "per_page": per_page,
            "page": page,
            "include": "tickets(users,organizations,groups)",
        }

        params = {key: value for key, value in params.items() if value is not None}

        response = client.get_request(
            entity="search",
            params=params,
        )

        tickets: List[Ticket] = [
            Ticket(
                ticket_id=str(ticket.get("id", "")),
                description=ticket.get("description"),
                status=ticket.get("status", ""),
                subject=ticket.get("subject"),
                created_at=ticket.get("created_at"),
                assignee_name=(
                    get_name_by_id(response.get("users", []), ticket.get("assignee_id"))
                    if ticket.get("assignee_id")
                    else None
                ),
                submitter_name=(
                    get_name_by_id(response.get("users", []), ticket.get("submitter_id"))
                    if ticket.get("submitter_id")
                    else None
                ),
                requester_name=(
                    get_name_by_id(response.get("users", []), ticket.get("requester_id"))
                    if ticket.get("requester_id")
                    else None
                ),
                organization_name=(
                    get_name_by_id(response.get("organizations", []), ticket.get("organization_id"))
                    if ticket.get("organization_id")
                    else None
                ),
                group_name=(
                    get_name_by_id(response.get("groups", []), ticket.get("group_id"))
                    if ticket.get("group_id")
                    else None
                ),
                priority=ticket.get("priority"),
                custom_fields=get_custom_field_key_id(
                    ticket.get("custom_fields", []), custom_field_name
                ),
            )
            for ticket in response.get("results", [])
        ]

        # Extract page and per_page from next_page if it exists
        output_page = None
        output_per_page = None
        next_api_link = response.get("next_page")
        if next_api_link is not None:
            query_params = get_query_param_from_links(next_api_link)
            output_page = int(query_params["page"]) if "page" in query_params else None
            output_per_page = int(query_params["per_page"]) if "per_page" in query_params else None

        return GetTicketsResponse(
            tickets=tickets,
            page=output_page,
            per_page=output_per_page,
        )

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        error_message = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return GetTicketsResponse(
            tickets=[],
            page=None,
            per_page=None,
            http_code=e.response.status_code,
            error_message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return GetTicketsResponse(
            tickets=[],
            page=None,
            per_page=None,
            http_code=500,
            error_message=str(e),
        )
