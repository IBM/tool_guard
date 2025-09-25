from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class AssignmentGroup:
    """Represents the details of the assignment groups in ServiceNow."""

    system_id: str
    assignment_group: str


@dataclass
class GetAssignmentGroupsResponse:
    """Represents the response from getting assignment groups in serviceNow."""

    assignment_groups: list[AssignmentGroup]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_assignment_groups(
    assignment_group: Optional[str] = None, system_id: Optional[str] = None
) -> GetAssignmentGroupsResponse:
    """
    Gets a list of assignment groups in Servicenow.

    Args:
        assignment_group: The name of the assignment group.
        system_id: The system ID of the assignment group.

    Returns:
        A list of all the assignment groups.
    """

    client = get_servicenow_client()
    params = {"name": assignment_group, "sys_id": system_id}
    params = {key: value for key, value in params.items() if value}
    response = client.get_request(entity="sys_user_group", params=params)

    assignment_groups_list = [
        AssignmentGroup(
            system_id=assignmentgroup.get("sys_id", ""),
            assignment_group=assignmentgroup.get("name", ""),
        )
        for assignmentgroup in response["result"]
    ]

    return GetAssignmentGroupsResponse(assignment_groups=assignment_groups_list)
