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
class CalendarInfo:
    """Represents the calendar details in Microsoft Outlook."""

    calendar_id: str
    calendar_name: str
    owner_name: str


@dataclass
class CalendarsInfoResponse:
    """Represents the list of calendars in Microsoft Outlook."""

    calendars: Optional[List[CalendarInfo]] = None
    limit: Optional[int] = None
    skip: Optional[int] = None
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_calendars(
    calendar_name: Optional[str] = None, limit: Optional[int] = 100, skip: Optional[int] = 0
) -> CalendarsInfoResponse:
    """
    Gets all calendars in Microsoft Outlook.

    Args:
        calendar_name: The name of the calendar in Microsoft Outlook.
        limit: The maximum number of calendars to retrieve in a single API call. Defaults to 100.
            Use this to control the size of the result set.
        skip: The number of calendars to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        The list of calendars.
    """
    client = get_microsoft_client()

    params: Dict[str, Any] = {}
    if calendar_name:
        params["$filter"] = f"name eq '{calendar_name}'"
    if limit:
        params["$top"] = limit
    if skip:
        params["$skip"] = skip

    endpoint = f"{client.get_user_resource_path()}/calendars"

    try:
        response = client.get_request(endpoint=endpoint, params=params)

        calendars = [
            CalendarInfo(
                calendar_id=result.get("id", ""),
                calendar_name=result.get("name", ""),
                owner_name=result.get("owner", {}).get("name", ""),
            )
            for result in response.get("value", [])
        ]

        output_limit = None
        output_skip = None
        next_api_link = response.get("@odata.nextLink", "")
        if next_api_link:
            query_params = get_query_param_from_links(next_api_link)
            output_limit = int(query_params["$top"])
            output_skip = int(query_params["$skip"])

        return CalendarsInfoResponse(
            calendars=calendars,
            limit=output_limit,
            skip=output_skip,
        )

    except HTTPError as e:
        error_message = ""
        try:
            error_response = e.response.json()
            error_message = error_response.get("error", {}).get("message", "")
        except json.JSONDecodeError:
            error_message = e.response.text or "An HTTP error occurred without a JSON response."

        return CalendarsInfoResponse(
            calendars=None,
            limit=None,
            skip=None,
            http_code=e.response.status_code,
            error_message=error_message,
        )

    except Exception as e:  # pylint: disable=broad-except
        return CalendarsInfoResponse(
            calendars=None,
            limit=None,
            skip=None,
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_message=str(e),
        )
