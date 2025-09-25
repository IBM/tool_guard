import json
from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_schemas import (
    TicketComponent,
    TicketPriority,
    TicketType,
)
from agent_ready_tools.tools.IT.zendesk.zendesk_utility import validate_enum_value
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class ZendeskCreateTicketResponse:
    """Represents the result of creating a ticket in Zendesk."""

    ticket_id: Optional[str] = None
    ticket_comment: Optional[str] = None
    ticket_subject: Optional[str] = None
    ticket_priority: Optional[str] = None
    http_code: Optional[int] = None
    error_message: Optional[str] = None
    error_description: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def zendesk_create_a_ticket(
    ticket_comment: str,
    ticket_subject: str,
    ticket_priority: str,
    group_id: Optional[int] = None,
    ticket_type: Optional[str] = None,
    ticket_component: Optional[str] = None,
    custom_fields: Optional[Dict[str, Any]] = None,
) -> ZendeskCreateTicketResponse:
    """
    Creates a ticket in Zendesk.

    Args:
        ticket_comment: The comment to be mentioned in the ticket.
        ticket_subject: The subject of the ticket.
        ticket_priority: The priority of the ticket (e.g, 'URGENT', 'HIGH', 'NORMAL', or 'LOW').
        group_id: The id of the assignee group to which this ticket is assigned, returned by the tool `get_all_groups`.
        ticket_type: The type of the ticket (e.g, 'PROBLEM', 'INCIDENT', 'QUESTION', or 'TASK').
        ticket_component: The component of the ticket(e.g, 'CORE_ITEM', 'ACCESSORIES', 'WARRANTIES').
        custom_fields: The custom fields associated with the ticket.

    Returns:
        Details of the created ticket.
    """
    try:
        client = get_zendesk_client()

        priority_value = validate_enum_value(ticket_priority, TicketPriority, "Ticket Priority")
        type_value = validate_enum_value(ticket_type, TicketType, "Ticket Type")
        component_value = validate_enum_value(ticket_component, TicketComponent, "Ticket Component")

        ticket_data: dict[str, Any] = {
            "comment": {"body": ticket_comment},
            "subject": ticket_subject,
            "group_id": group_id,
            "custom_fields": custom_fields,
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
        if type_value:
            ticket_data["type"] = type_value
        if component_value:
            ticket_data["tags"] = [component_value]

        payload = {"ticket": ticket_data}
        response = client.post_request(entity="tickets", payload=payload)
        ticket_result = response.get("tickets", {})

        return ZendeskCreateTicketResponse(
            ticket_id=str(ticket_result.get("id")),
            ticket_comment=str(ticket_result.get("description")),
            ticket_subject=str(ticket_result.get("subject")),
            ticket_priority=str(ticket_result.get("priority")),
            http_code=response.get("status_code", 200),
        )
    except HTTPError as e:
        error_response = e.response.json()
        error_message = error_response.get("error", "")
        error_description = error_response.get("description", "")
        return ZendeskCreateTicketResponse(
            http_code=e.response.status_code,
            error_message=error_message,
            error_description=error_description,
        )
    except Exception as e:  # pylint: disable=broad-except
        error_message = str(e)
        return ZendeskCreateTicketResponse(
            http_code=500,
            error_message=error_message,
            error_description="An unexpected error occurred.",
        )
