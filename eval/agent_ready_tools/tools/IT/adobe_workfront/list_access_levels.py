from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class AccessLevel:
    """Represents a single access level in Adobe Workfront."""

    access_level_id: str
    access_level_name: str
    access_level_restrictions: str
    license_type: str


@dataclass
class ListAccessLevelsResponse:
    """Represents the response for retrieving access levels in Adobe Workfront."""

    access_levels: List[AccessLevel]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def list_access_levels(
    access_level_name: Optional[str] = None, limit: Optional[int] = 50, skip: Optional[int] = 0
) -> ListAccessLevelsResponse:
    """
    Gets a list of access levels from Adobe Workfront.

    Args:
        access_level_name: The name of the access level in Adobe Workfront.
        limit: The maximum number of access level to retrieve in a single API call. Defaults to 50.
            Use this to control the size of the result set.
        skip: The number of access level to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        List of accesslevels.
    """
    client = get_adobe_workfront_client()

    params = {"name": access_level_name, "$$LIMIT": limit, "$$SKIP": skip}

    # Filters out the parameter that are None/Blank.
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="accessLevel/search", params=params)

    access_levels: List[AccessLevel] = [
        AccessLevel(
            access_level_id=result.get("ID", ""),
            access_level_name=result.get("name", ""),
            access_level_restrictions=result.get("accessRestrictions", ""),
            license_type=result.get("licenseType", ""),
        )
        for result in response.get("data", [])
    ]

    return ListAccessLevelsResponse(
        access_levels=access_levels,
    )
