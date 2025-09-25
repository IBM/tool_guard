from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class DeleteATicketResponse:
    """Represents the result of an ticket delete operation in Service Now."""

    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def delete_a_ticket(ticket_number_system_id: str) -> DeleteATicketResponse:
    """
    Deletes a ticket in ServiceNow.

    Args:
        ticket_number_system_id: The system_id of the ticket number returned by the `get_tickets`
            tool.

    Returns:
        The result from performing the delete a ticket.
    """

    client = get_servicenow_client()

    response = client.delete_request(entity="ticket", entity_id=f"{ticket_number_system_id}")
    return DeleteATicketResponse(http_code=response)
