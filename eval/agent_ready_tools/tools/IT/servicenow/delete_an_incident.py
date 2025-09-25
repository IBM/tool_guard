from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class DeleteIncidentResponse:
    """Represents the delete response of the incident in ServiceNow."""

    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def delete_an_incident(incident_number_system_id: str) -> DeleteIncidentResponse:
    """
    Deletes an incident in ServiceNow.

    Args:
        incident_number_system_id: The system_id of the incident returned by the `get_incidents`
            tool.

    Returns:
        Confirmation of an incident deletion.
    """

    client = get_servicenow_client()

    response = client.delete_request(entity="incident", entity_id=incident_number_system_id)
    return DeleteIncidentResponse(http_code=response)
