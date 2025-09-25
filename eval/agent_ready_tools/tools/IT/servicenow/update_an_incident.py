from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class UpdateIncidentResponse:
    """Represents the update response of the incident in ServiceNow."""

    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def update_an_incident(
    incident_number_system_id: str,
    state_code: Optional[str] = None,
    urgency_value: Optional[str] = None,
    impact_value: Optional[str] = None,
    assignment_group_system_id: Optional[str] = None,
    assigned_to_user_system_id: Optional[str] = None,
    category_system_id: Optional[str] = None,
    short_description: Optional[str] = None,
    description: Optional[str] = None,
    close_notes: Optional[str] = None,
    comments: Optional[str] = None,
    work_notes: Optional[str] = None,
    expected_start_date: Optional[str] = None,
    work_start_date: Optional[str] = None,
    due_date: Optional[str] = None,
) -> UpdateIncidentResponse:
    """
    Updates an incident in ServiceNow.

    Args:
        incident_number_system_id: The system_id of the incident number returned by the
            `get_incidents` tool.
        state_code: The state value of the incident returned by the tool `get_states`.
        urgency_value: The urgency value of the incident returned by the tool `get_urgencies`.
        impact_value: The impact level of the incident returned by the `get_impacts` tool.
        assignment_group_system_id: The system_id of the assignment group name returned by the
            `get_assignment_groups` tool.
        assigned_to_user_system_id: The system_id of the user name returned by the
            `get_system_users` tool.
        category_system_id: The system_id of the category to which the incident belongs returned by
            the tool `get_categories`.
        short_description: A brief summary of the incident.
        description: A detailed description of the incident, including any relevant information or
            steps to reproduce the issue.
        close_notes: Notes added when closing the incident, explaining the resolution or any actions
            taken.
        comments: Additional comments or updates related to the incident.
        work_notes: Additional work_notes or updates related to the incident.
        expected_start_date: The expected start date of the incident in ISO 8601 format (e.g., YYYY-
            MM-DD).
        work_start_date: The work start date of the incident in ISO 8601 format (e.g., YYYY-MM-DD).
        due_date: The due date for the incident in ISO 8601 format (e.g., YYYY-MM-DD).

    Returns:
        The result from performing the update an incident.
    """

    client = get_servicenow_client()
    payload = {
        "short_description": short_description,
        "description": description,
        "state": state_code,
        "urgency": urgency_value,
        "impact": impact_value,
        "assignment_group": assignment_group_system_id,
        "assigned_to": assigned_to_user_system_id,
        "category": category_system_id,
        "close_notes": close_notes,
        "comments": comments,
        "work_notes": work_notes,
        "expected_start": expected_start_date,
        "work_start": work_start_date,
        "due_date": due_date,
    }

    payload = {key: value for key, value in payload.items() if value}

    response = client.patch_request(
        entity="incident",
        entity_id=incident_number_system_id,
        payload=payload,
    )
    return UpdateIncidentResponse(http_code=response["status_code"])
