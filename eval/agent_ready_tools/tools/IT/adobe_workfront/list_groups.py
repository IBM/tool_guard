from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class Groups:
    """Represents the class for retrieving groups in Adobe Workfront."""

    group_id: str
    group_name: str
    public_visibility: bool
    group_description: Optional[str]
    object_code: Optional[str]


@dataclass
class ListGroupsResponse:
    """Represents the response for retrieving groups in Adobe Workfront."""

    groups: List[Groups]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def list_groups(
    group_name: Optional[str] = None,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0,
) -> ListGroupsResponse:
    """
    Gets a list of groups from Adobe Workfront.

    Args:
        group_name: The name of the group in Adobe Workfront.
        limit: The maximum number of groups to return. Default is 100.
        skip: The number of groups to skip (for pagination). Default is 0.

    Returns:
        List of groups.
    """

    client = get_adobe_workfront_client()
    params = {"name": group_name, "$$LIMIT": limit, "$$FIRST": skip}

    params = {key: value for key, value in params.items() if value is not None}
    response = client.get_request(entity="group/search", params=params)

    groups: List[Groups] = [
        Groups(
            group_id=result.get("ID", ""),
            group_name=result.get("name", ""),
            group_description=result.get("description", ""),
            public_visibility=result.get("isPublic", ""),
            object_code=result.get("objCode", ""),
        )
        for result in response.get("data", [])
    ]

    return ListGroupsResponse(
        groups=groups,
    )
