from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class Teams:
    """Represents the details of a team in Microsoft Teams."""

    team_id: str
    team_name: str
    team_description: Optional[str] = None


@dataclass
class TeamsResponse:
    """Represents a list of teams in Microsoft Teams."""

    teams: List[Teams]
    limit: Optional[int] = 0
    skip_token: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_teams(
    team_name: Optional[str] = None, limit: Optional[int] = 50, skip_token: Optional[str] = None
) -> TeamsResponse:
    """
    Retrieves a list of teams in Microsoft Teams.

    Args:
        team_name: The team_name is used to filter results in Microsoft Teams based upon the
            team_name.
        limit: The maximum number of teams retrieved in a single API call. Defaults to 50. Use this
            to control the size of the result set in Microsoft Teams.
        skip_token: A token used to skip a specific number of items for pagination purposes. Use
            this to retrieve subsequent pages of results when handling large datasets.

    Returns:
        List of all the teams in Microsoft Teams, along with pagination parameters (limit and skip).
    """

    client = get_microsoft_client()
    params = {
        "$top": limit,
        "$skiptoken": skip_token,
        "$select": "id, displayName, description",
        "$filter": f"displayName eq '{team_name}'" if team_name else "",
    }
    # Filter out the paramaters that are None/Blank.
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(endpoint=f"teams", params=params)

    # Extract limit and skiptoken from @odata.nextLink if it exists

    next_api_link = response.get("@odata.nextLink", "")
    if next_api_link:
        query_params = get_query_param_from_links(href=next_api_link)
        output_limit = query_params.get("$top", "")
        output_skip_token = query_params.get("$skiptoken", "")
    else:
        output_limit = limit
        output_skip_token = skip_token

    teams_list: List[Teams] = []

    for team in response["value"]:
        teams_list.append(
            Teams(
                team_id=team.get("id", ""),
                team_name=team.get("displayName", ""),
                team_description=team.get("description", ""),
            )
        )

    return TeamsResponse(teams=teams_list, limit=int(output_limit), skip_token=output_skip_token)
