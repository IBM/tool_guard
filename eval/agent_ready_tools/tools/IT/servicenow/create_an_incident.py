from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class CreateIncident:
    """Represents the result of create an incident in ServiceNow."""

    system_id: str
    incident_number: str
    short_description: str
    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def create_an_incident(
    short_description: str,
    impact_value: str,
    urgency_value: str,
    incident_category: Optional[str] = None,
    assignment_group: Optional[str] = None,
    description: Optional[str] = None,
    caller_username: Optional[str] = None,
) -> CreateIncident:
    """
    Creates an incident in ServiceNow.

    Args:
        short_description: A brief summary of the incident in ServiceNow.
        impact_value: The impact_value is returned by the tool `get_impacts`.
        urgency_value: The urgency_value is returned by the tool `get_urgencies`.
        incident_category: The category_name is returned by the tool `get_categories`.
        assignment_group: The name of the assignment group returned by the tool
            `get_assignment_groups`.
        description: The description for the incident in ServiceNow.
        caller_username: The caller username is returned by the tool `get_system_users`.

    Returns:
        The result from performing the create an incident.
    """
    client = get_servicenow_client()

    payload = {
        "short_description": short_description,
        "impact": impact_value,
        "urgency": urgency_value,
        "category": incident_category,
        "assignment_group": assignment_group,
        "description": description,
        "caller_id": caller_username,
    }
    response = client.post_request(entity="incident", payload=payload)

    result = response.get("result", None)

    return CreateIncident(
        incident_number=result and result.get("number", ""),
        short_description=result and result.get("short_description", ""),
        http_code=response.get("status_code", ""),
        system_id=result.get("sys_id", ""),
    )
