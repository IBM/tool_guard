from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class PermissionGroup:
    """Represents the class for retrieving the Permission groups in Zendesk."""

    permission_group_id: str
    permission_group_name: str


@dataclass
class ListPermissionGroupResponse:
    """Represents the response for retrieving permission groups in Zendesk."""

    permission_groups: List[PermissionGroup]
    page: Optional[int]
    per_page: Optional[int]
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def list_permission_groups(
    permission_group_name: Optional[str] = None,
    per_page: Optional[int] = 10,
    page: Optional[int] = 1,
) -> ListPermissionGroupResponse:
    """
    Gets a list of permission groups from Zendesk.

    Args:
        permission_group_name: The name of the permission group in Zendesk.
        per_page: Number of permission groups to retrieve per page. Defaults to 10.
        page: Page number to retrieve. Defaults to 1.

    Returns:
        List of permission group.
    """

    try:
        client = get_zendesk_client()

        params = {"name": permission_group_name, "per_page": per_page, "page": page}

        params = {key: value for key, value in params.items() if value}

        entity = "guide/permission_groups"
        response = client.get_request(entity=entity, params=params)

        permission_groups: List[PermissionGroup] = [
            PermissionGroup(
                permission_group_id=str(result.get("id", "")),
                permission_group_name=result.get("name", ""),
            )
            for result in response.get("permission_groups", [])
        ]

        # Extract page and per_page from next_page if it exists
        output_page = None
        output_per_page = None
        next_api_link = response.get("next_page")
        if next_api_link is not None:
            query_params = get_query_param_from_links(next_api_link)
            output_page = int(query_params["page"]) if "page" in query_params else None
            output_per_page = int(query_params["per_page"]) if "per_page" in query_params else None

        return ListPermissionGroupResponse(
            permission_groups=permission_groups,
            page=output_page,
            per_page=output_per_page,
        )

    except HTTPError as e:
        error_response = e.response.json()
        error_message = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return ListPermissionGroupResponse(
            permission_groups=[],
            page=None,
            per_page=None,
            http_code=e.response.status_code,
            error_message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return ListPermissionGroupResponse(
            permission_groups=[],
            page=None,
            per_page=None,
            http_code=500,
            error_message=str(e),
        )
