from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from requests.exceptions import HTTPError, RequestException

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseTeamTemplate
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def create_predefined_case_team(
    name: str,
    description: Optional[str] = None,
) -> CaseTeamTemplate:
    """
    Creates a predefined case team in Salesforce.

    Args:
        name: The unique name of the predefined case team to be created.
        description: The description of the case team.

    Returns:
        The result of create operation for a predefined case team.
    """

    client = get_salesforce_client()

    data = {
        "Name": name,
        "Description": description,
    }

    # Filter out any parameters that are None
    data = {key: value for key, value in data.items() if value}

    try:
        response = client.salesforce_object.CaseTeamTemplate.create(data)  # type: ignore[operator]
        return CaseTeamTemplate(
            id=response.get("id"),
            name=name,
            description=description,
        )
    except HTTPError as e:
        error_response = e.response.json()
        error_message = error_response.get("error", {}).get("code", "")
        error_description = error_response.get("error", {}).get("message", "")
        return CaseTeamTemplate(
            error_message=error_message,
            error_description=error_description,
        )
    except RequestException as e:  # pylint: disable=broad-except
        error_message = str(e)
        return CaseTeamTemplate(
            error_message=error_message,
            error_description="An unexpected error occurred.",
        )
