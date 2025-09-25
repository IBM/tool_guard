from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class Incidents:
    """Represents the details of the incident in ServiceNow."""

    incident_number: str
    state: str
    priority: str
    system_id: str
    impact: str
    urgency: str
    category: str
    short_description: Optional[str] = None
    assigned_to_user: Optional[str] = None
    caller_username: Optional[str] = None
    due_date: Optional[str] = None
    comments_and_work_notes: Optional[str] = None
    description: Optional[str] = None
    assignment_group: Optional[str] = None
    created_on: Optional[str] = None
    opened_at: Optional[str] = None
    closed_at: Optional[str] = None


@dataclass
class IncidentsResponse:
    """Represents list of incidents in ServiceNow."""

    incidents: list[Incidents]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_incidents(
    search: Optional[str] = None, limit: Optional[int] = 10, skip: Optional[int] = 0
) -> IncidentsResponse:
    """
    Retrieves a list of incidents in ServiceNow.

    Args:
        search: Searches for incidents using a search parameter with zero, one, or more of the
            optional filters.[eg.number, opened_at, short_description, created_at]
        limit: The maximum number of incidents to retrieve in a single API call. Defaults to 10. Use
            this to control the size of the result set.
        skip: The number of incidents to skip for pagination

    Returns:
        A list of all the incidents.
    """

    client = get_servicenow_client()
    params = {
        "sysparm_query": search,
        "sysparm_display_value": True,
        "sysparm_limit": limit,
        "sysparm_offset": skip,
    }

    params = {key: value for key, value in params.items() if value is not None}

    response = client.get_request(entity="incident", params=params)

    incidents_list: list[Incidents] = []

    for incident in response["result"]:

        incidents_list.append(
            Incidents(
                incident_number=incident.get("number", ""),
                state=incident.get("state", ""),
                priority=incident.get("priority", ""),
                short_description=incident.get("short_description", ""),
                system_id=incident.get("sys_id", ""),
                assigned_to_user=(
                    incident.get("assigned_to", {}).get("display_value", "")
                    if isinstance(incident.get("assigned_to"), dict)
                    else incident.get("assigned_to", "")
                ),
                caller_username=(
                    incident.get("caller_id", {}).get("display_value", "")
                    if isinstance(incident.get("caller_id"), dict)
                    else incident.get("caller_id", "")
                ),
                due_date=incident.get("due_date", ""),
                comments_and_work_notes=incident.get("comments_and_work_notes", ""),
                impact=incident.get("impact", ""),
                urgency=incident.get("urgency", ""),
                description=incident.get("description", ""),
                assignment_group=(
                    incident.get("assignment_group", {}).get("display_value", "")
                    if isinstance(incident.get("assignment_group"), dict)
                    else incident.get("assignment_group", "")
                ),
                category=incident.get("category", ""),
                created_on=incident.get("sys_created_on", ""),
                opened_at=incident.get("opened_at", ""),
                closed_at=incident.get("closed_at", ""),
            )
        )
    return IncidentsResponse(incidents=incidents_list)
