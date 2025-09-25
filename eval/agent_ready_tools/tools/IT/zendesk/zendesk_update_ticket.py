import json
from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_schemas import TicketPriority
from agent_ready_tools.tools.IT.zendesk.zendesk_utility import validate_enum_value
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class ZendeskUpdateTicketResponse:
    """Represents the result of updating a ticket in Zendesk."""

    ticket_id: Optional[int] = None
    ticket_status: Optional[str] = None
    ticket_subject: Optional[str] = None
    assignee_id: Optional[int] = None
    http_code: Optional[int] = None
    error_description: Optional[str] = None
    ticket_priority: Optional[TicketPriority] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def zendesk_update_ticket(
    ticket_id: int,
    ticket_status: Optional[str] = None,
    ticket_priority: Optional[str] = None,
    ticket_subject: Optional[str] = None,
    assignee_id: Optional[int] = None,
    ticket_comment: Optional[str] = None,
    group_id: Optional[int] = None,
    custom_fields: Optional[Dict[str, Any]] = None,
) -> ZendeskUpdateTicketResponse:
    """
    Updates a ticket in Zendesk.

    Args:
        ticket_id: The id of the ticket to be updated, returned by the `get_tickets` tool.
        ticket_status: The status of the ticket, returned by the `get_ticket_statuses` tool.
        ticket_priority: The priority of the ticket (e.g, 'URGENT', 'HIGH', 'NORMAL', or 'LOW').
        ticket_subject: The subject or title of the ticket.
        assignee_id: The id of the user to whom the ticket should be assigned, returned by the `get_users` tool.
        ticket_comment: The comment which you can update in ticket.
        group_id: The id of the group to assign the ticket to. Typically returned by the `get_groups` tool.
        custom_fields: The custom fields associated with the ticket.

    Returns:
        The updated ticket details.
    """

    try:
        client = get_zendesk_client()
        priority_value = validate_enum_value(ticket_priority, TicketPriority, "Ticket Priority")

        ticket_data: dict[str, Any] = {
            "status": ticket_status,
            "subject": ticket_subject,
            "assignee_id": assignee_id,
            "group_id": group_id,
            "custom_fields": custom_fields,
            "comment": {"body": ticket_comment} if ticket_comment else None,
        }
        # Handling custom fields
        if custom_fields:
            custom_fields_dict = (
                json.loads(custom_fields) if isinstance(custom_fields, str) else custom_fields
            )
            ticket_data["custom_fields"] = custom_fields_dict

        # Filter out the parameters that are None/Blank.
        ticket_data = {key: value for key, value in ticket_data.items() if value}

        if priority_value:
            ticket_data["priority"] = priority_value

        payload = {"ticket": ticket_data}

        response = client.put_request(entity=f"tickets/{ticket_id}", payload=payload)

        ticket = response.get("ticket", {})

        return ZendeskUpdateTicketResponse(
            ticket_id=ticket.get("id", ticket_id),
            ticket_status=ticket.get("status", ""),
            ticket_priority=ticket.get("priority", ""),
            ticket_subject=ticket.get("subject", ""),
            assignee_id=ticket.get("assignee_id", ""),
        )

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else {}
        error = error_response.get("error", "")
        if isinstance(error, dict):
            error_description = error.get("message", "")
        else:
            error_description = error_response.get("details", {}).get("subject", [{}])[0].get(
                "description", ""
            ) or error_response.get("error", "")
            http_code = e.response.status_code

        return ZendeskUpdateTicketResponse(
            error_description=error_description,
            http_code=http_code,
        )

    except Exception as e:  # pylint: disable=broad-except
        return ZendeskUpdateTicketResponse(
            error_description=f"An unexpected error occurred. {e}",
        )
