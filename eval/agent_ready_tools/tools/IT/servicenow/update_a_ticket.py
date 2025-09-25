from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class UpdateTicket:
    """Represents the result of the ticket update in ServiceNow."""

    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def update_a_ticket(
    ticket_number_system_id: str,
    description: Optional[str] = None,
    parent_task_number: Optional[str] = None,
    due_date: Optional[str] = None,
    state_code: Optional[str] = None,
    short_description: Optional[str] = None,
    priority: Optional[str] = None,
    urgency_value: Optional[str] = None,
    impact_value: Optional[str] = None,
    assignment_group: Optional[str] = None,
    assigned_to_user: Optional[str] = None,
    comments: Optional[str] = None,
    work_notes: Optional[str] = None,
) -> UpdateTicket:
    """
    Updates the ticket details in ServiceNow.

    Args:
        ticket_number_system_id: The system_id of the ticket as the value will be fetched from
            `get_all_tickets` tool.
        description: A detailed explanation of the ticket.
        parent_task_number: The parent task number for the ticket.
        due_date: The due date to resolve the ticket in ISO 8601 format (e.g., YYYY-MM-DD).
        state_code: The state of the ticket, returned by the tool `get_states`.
        short_description: The short description of the ticket.
        priority: The priority of the ticket, returned by the tool `get_priorities`.
        urgency_value: The urgency_value of a ticket, returned by the tool `get_urgencies`.
        impact_value: The impact_value of a ticket, returned by the tool `get_impacts`.
        assignment_group: The name of the assignment group returned by the tool
            `get_assignment_groups`.
        assigned_to_user: The name of the user to whom the ticket is assigned, it is returned by the
            tool `get_system_users`.
        comments: Additional comments or updates related to the ticket.
        work_notes: Additional work notes or updates related to the ticket.

    Returns:
        The result from performing the update a ticket.
    """

    client = get_servicenow_client()

    payload: dict[str, Any] = {
        "description": description,
        "parent": parent_task_number,
        "due_date": due_date,
        "state": state_code,
        "short_description": short_description,
        "priority": priority,
        "urgency": urgency_value,
        "impact": impact_value,
        "assignment_group": assignment_group,
        "assigned_to": assigned_to_user,
        "comments": comments,
        "work_notes": work_notes,
    }
    # Filter out the blank parameters.
    payload = {key: value for key, value in payload.items() if value}

    params = {"sysparm_display_value": True}

    response = client.patch_request(
        entity="ticket", entity_id=ticket_number_system_id, payload=payload, params=params
    )

    return UpdateTicket(http_code=response["status_code"])
