from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class CreateTicketResponse:
    """Represents the result of creating a ticket in ServiceNow."""

    system_id: str
    ticket_number: str
    short_description: str
    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def create_a_ticket(
    short_description: str,
    priority: str,
    assignment_group: Optional[str] = None,
    parent_task_number: Optional[str] = None,
    description: Optional[str] = None,
) -> CreateTicketResponse:
    """
    Creates a ticket in ServiceNow.

    Args:
        short_description: A brief summary of the ticket.
        priority: The priority of the ticket, returned by the tool `get_priorities`.
        assignment_group: The name of the assignment group returned by the tool
            `get_assignment_groups`.
        parent_task_number: The parent task number for the ticket.
        description: A detailed explanation of the ticket.

    Returns:
        The result from performing the creation of a ticket.
    """
    client = get_servicenow_client()

    payload = {
        "short_description": short_description,
        "assignment_group": assignment_group,
        "parent": parent_task_number,
        "description": description,
        "priority": priority,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="ticket", payload=payload)
    result = response.get("result", {})
    return CreateTicketResponse(
        system_id=result.get("sys_id", ""),
        ticket_number=result.get("number", ""),
        short_description=result.get("short_description", ""),
        http_code=response.get("status_code", ""),
    )
