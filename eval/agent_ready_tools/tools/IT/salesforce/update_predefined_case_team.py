from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_predefined_case_team(
    team_template_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> int:
    """
    Updates an existing predefined case team in Salesforce.

    Args:
        team_template_id: The id of the predefined case team in Salesforce returned by the tool
            `get_predefined_case_teams`.
        name: The new name for the predefined case team.
        description: The new description for the case team.

    Returns:
        The status of the update operation performed on the predefined case team.
    """

    client = get_salesforce_client()

    data = {
        "Name": name,
        "Description": description,
    }

    # Filter out the blank parameters
    data = {key: value for key, value in data.items() if value is not None}

    status = client.salesforce_object.CaseTeamTemplate.update(team_template_id, data)  # type: ignore[operator]

    return status
