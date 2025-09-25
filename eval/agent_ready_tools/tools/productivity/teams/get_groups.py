from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class Group:
    """Represents a group in Microsoft Teams."""

    group_name: str
    group_id: str
    group_mail: Optional[str]
    group_description: Optional[str]
    group_created_date_time: str
    group_visibility: Optional[str]


@dataclass
class GetGroupsResponse:
    """Represents the list of groups in Microsoft Teams."""

    groups: List[Group]
    limit: Optional[int] = 0
    skip_token: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_groups(
    group_mail: Optional[str] = None, limit: Optional[int] = 100, skip_token: Optional[str] = None
) -> GetGroupsResponse:
    """
    Retrieves a list of groups in Microsoft Teams.

    Args:
        group_mail: The email of the group to be used as a filter in Microsoft Teams.
        limit: The maximum number of groups retrieved in a single API call. Defaults to 100. Use
            this to control the size of the result set in Microsoft Teams.
        skip_token: A token used to skip a specific number of items for pagination purposes. Use
            this to retrieve subsequent pages of results when handling large datasets.

    Returns:
        List of all the groups in Microsoft Teams, along with pagination parameters (limit and
        skip_token).
    """

    client = get_microsoft_client()
    filter_string = f"mail eq '{group_mail}'" if group_mail else None
    params = {
        "$top": limit,
        "$skiptoken": skip_token,
        "$filter": filter_string,
    }

    # Filter out the parameters that are None/Blank.
    params = {key: value for key, value in params.items() if value}

    # Make the API request to get groups
    endpoint = "groups"
    response = client.get_request(endpoint=endpoint, params=params)
    # Mapping the response data to Group objects
    groups_list: List[Group] = []

    for result in response.get("value", []):
        groups_list.append(
            Group(
                group_name=result.get("displayName", ""),
                group_id=result.get("id", ""),
                group_mail=result.get("mail", ""),
                group_description=result.get("description", ""),
                group_created_date_time=result.get("createdDateTime", ""),
                group_visibility=result.get("visibility", ""),
            )
        )

    # Extract limit and skip from @odata.nextLink if it exists
    next_api_link = response.get("@odata.nextLink", "")
    output_limit = 0
    output_skip = None
    if next_api_link:
        query_params = get_query_param_from_links(href=next_api_link)
        output_limit = query_params.get("$top", "")
        output_skip = query_params.get("$skiptoken", "")
    return GetGroupsResponse(groups=groups_list, limit=int(output_limit), skip_token=output_skip)
