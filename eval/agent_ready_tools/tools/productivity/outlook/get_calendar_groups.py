from http import HTTPStatus
import json
from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class CalendarGroup:
    """Represents the details of a calendar group in Microsoft Outlook."""

    calendar_group_name: str
    calendar_group_class_id: str
    calendar_group_change_key: str
    calendar_group_id: str


@dataclass
class CalendarGroupsResponse:
    """Represents the list of calendar groups in Microsoft Outlook."""

    calendar_groups: Optional[List[CalendarGroup]] = None
    limit: Optional[int] = None
    skip: Optional[int] = None
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_calendar_groups(
    calendar_group_name: Optional[str] = None, limit: Optional[int] = 10, skip: Optional[int] = 0
) -> CalendarGroupsResponse:
    """
    Retrieves a list of calendar groups from Microsoft Outlook.

    Args:
        calendar_group_name: The name of the calendar group as a filter in Microsoft Outlook.
        limit: The maximum number of calendar groups to retrieve in a single API call. Defaults to
            10. Use this to control the size of the result set.
        skip: The number of calendar groups to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        List of calendar groups with their calendar_group_id, calendar_group_name,
        calendar_group_class_id, and calendar_group_change_key, along with pagination parameters
        (limit and skip).
    """
    client = get_microsoft_client()

    # Prepare parameters with filtering and pagination options
    params: Dict[str, Any] = {"$top": limit, "$skip": skip}
    if calendar_group_name:
        params["$filter"] = f"name eq '{calendar_group_name}'"
    try:
        response = client.get_request(
            endpoint=f"{client.get_user_resource_path()}/calendarGroups", params=params
        )

        calendar_groups: List[CalendarGroup] = [
            CalendarGroup(
                calendar_group_name=group.get("name", ""),
                calendar_group_class_id=group.get("classId", ""),
                calendar_group_change_key=group.get("changeKey", ""),
                calendar_group_id=group.get("id", ""),
            )
            for group in response.get("value", [])
        ]

        # Extract limit and skip from @odata.nextLink if it exists for pagination
        output_limit = None
        output_skip = None
        next_api_link = response.get("@odata.nextLink", "")
        if next_api_link:
            query_params = get_query_param_from_links(next_api_link)
            output_limit = int(query_params["$top"])
            output_skip = int(query_params["$skip"])

        return CalendarGroupsResponse(
            calendar_groups=calendar_groups,
            limit=output_limit,
            skip=output_skip,
        )
    except HTTPError as e:
        error_message = ""
        try:
            # Try to parse the JSON error response from the API
            error_response = e.response.json()
            error_message = error_response.get("error", {}).get("message", "")
        except json.JSONDecodeError:
            # Fallback for non-JSON error responses (e.g., HTML from a proxy)
            error_message = e.response.text or "An HTTP error occurred without a JSON response."

        return CalendarGroupsResponse(
            http_code=e.response.status_code,
            error_message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return CalendarGroupsResponse(
            error_message=str(e), http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
        )
