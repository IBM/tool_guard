from dataclasses import dataclass
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_utility import get_name_by_id
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class Group:
    """Represents a group in Zendesk."""

    group_id: str
    name: str
    is_public: bool
    created_at: str
    updated_at: str
    user_names: Optional[List[str]] = None
    description: Optional[str] = None


@dataclass
class GetGroupsResponse:
    """Represents the response for retrieving groups in Zendesk."""

    groups: List[Group]
    page: Optional[int]
    per_page: Optional[int]
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def zendesk_get_groups(
    search: Optional[str] = None, per_page: Optional[int] = 10, page: Optional[int] = 1
) -> GetGroupsResponse:
    """
    Gets groups from Zendesk.

    Args:
        search: Optional search query. Users can search for a group using a keyword (e.g., WO) or the complete group name (e.g., WO test).
        per_page: Number of groups to retrieve per page. Defaults to 10.
        page: Page number to retrieve. Defaults to 1.

    Returns:
        List of groups.
    """
    try:
        client = get_zendesk_client()
        query = "type:group " + search if search else "type:group"
        params = {
            "query": query,
            "per_page": per_page,
            "page": page,
            "include": "groups(users)",
        }

        params = {key: value for key, value in params.items() if value}

        response = client.get_request(
            entity="search",
            params=params,
        )

        groups: List[Group] = [
            Group(
                group_id=str(group.get("id", "")),
                name=group.get("name", ""),
                is_public=group.get("is_public", True),
                created_at=group.get("created_at", ""),
                updated_at=group.get("updated_at", ""),
                user_names=[
                    name
                    for user_id in group.get("user_ids", [])
                    for name in [get_name_by_id(response.get("users", []), user_id)]
                    if name is not None
                ],
                description=group.get("description", ""),
            )
            for group in response.get("results", [])
        ]
        output_page = None
        output_per_page = None
        next_api_link = response.get("next_page")
        if next_api_link is not None:
            query_params = get_query_param_from_links(next_api_link)
            output_page = int(query_params["page"]) if "page" in query_params else None
            output_per_page = int(query_params["per_page"]) if "per_page" in query_params else None

        return GetGroupsResponse(groups=groups, page=output_page, per_page=output_per_page)

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        error_message = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return GetGroupsResponse(
            groups=[],
            page=None,
            per_page=None,
            http_code=e.response.status_code,
            error_message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return GetGroupsResponse(
            groups=[],
            page=None,
            per_page=None,
            http_code=None,
            error_message=str(e),
        )
