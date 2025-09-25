from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class Ticket:
    """Represents the details of a single ticket in ServiceNow."""

    priority: str
    ticket_number: str
    assignment_group: str
    state: str
    system_id: str
    assigned_to_user: str
    created_on: str
    opened_at: str
    comments_and_work_notes: Optional[str] = None
    closed_at: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    short_description: Optional[str] = None


@dataclass
class TicketsResponse:
    """Represents a list of tickets in ServiceNow."""

    tickets: list[Ticket]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_tickets(
    search: Optional[str] = None, limit: Optional[int] = 10, skip: Optional[int] = 0
) -> TicketsResponse:
    """
    Gets a list of all tickets in ServiceNow.

    Args:
        search: Searches for incidents using a search parameter with zero, one, or more of the
            optional filters (eg.number, opened_at, short_description, created_at).
        limit: The maximum number of tickets to retrieve in a single API call. Defaults to 10. Use
            this to control the size of the result set.
        skip: The number of tickets to skip for pagination.

    Returns:
        A TicketsResponse containing a list of tickets.
    """
    client = get_servicenow_client()

    params = {
        "sysparm_query": search,
        "sysparm_display_value": True,
        "sysparm_limit": limit,
        "sysparm_offset": skip,
    }

    params = {key: value for key, value in params.items() if value is not None}

    response = client.get_request(entity="ticket", params=params)

    tickets = [
        Ticket(
            description=ticket_result.get("description", ""),
            priority=ticket_result.get("priority", ""),
            ticket_number=ticket_result.get("number", ""),
            due_date=ticket_result.get("due_date", ""),
            assignment_group=(
                ticket_result.get("assignment_group", {}).get("display_value", "")
                if isinstance(ticket_result.get("assignment_group"), dict)
                else ticket_result.get("assignment_group", "")
            ),
            state=ticket_result.get("state", ""),
            short_description=ticket_result.get("short_description", ""),
            comments_and_work_notes=ticket_result.get("comments_and_work_notes", ""),
            system_id=ticket_result.get("sys_id", ""),
            assigned_to_user=(
                ticket_result.get("assigned_to", {}).get("display_value", "")
                if isinstance(ticket_result.get("assigned_to"), dict)
                else ticket_result.get("assigned_to", "")
            ),
            created_on=ticket_result.get("sys_created_on", ""),
            opened_at=ticket_result.get("opened_at", ""),
            closed_at=ticket_result.get("closed_at", ""),
        )
        for ticket_result in response.get("result", [])
    ]

    return TicketsResponse(tickets)
