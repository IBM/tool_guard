from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class UserSegment:
    """Represents the class for retrieving the user segments in Zendesk."""

    user_segment_id: str
    user_type: str
    user_segment_name: str


@dataclass
class ListuserSegmentsResponse:
    """Represents the response for retrieving user segments in Zendesk."""

    user_segments: List[UserSegment]
    per_page: Optional[int]
    page: Optional[int]
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def list_user_segments(
    user_segment_name: Optional[str] = None, per_page: Optional[int] = 10, page: Optional[int] = 0
) -> ListuserSegmentsResponse:
    """
    Gets a list of user segment from Zendesk.

    Args:
        user_segment_name: The name of the user segment in Zendesk.
        per_page: Number of user segments to retrieve per page. Defaults to 10.
        page: Page number to retrieve. Defaults to 1.

    Returns:
        List of user segments.
    """
    try:
        client = get_zendesk_client()

        params = {"name": user_segment_name, "per_page": per_page, "page": page}

        params = {key: value for key, value in params.items() if value}

        entity = "help_center/user_segments"
        response = client.get_request(entity=entity, params=params)

        user_segment: List[UserSegment] = [
            UserSegment(
                user_segment_id=str(result.get("id", "")),
                user_type=result.get("user_type", ""),
                user_segment_name=result.get("name", ""),
            )
            for result in response.get("user_segments", [])
        ]

        output_page = None
        output_per_page = None
        next_api_link = response.get("next_page")
        if next_api_link is not None:
            query_params = get_query_param_from_links(next_api_link)
            output_page = int(query_params["page"]) if "page" in query_params else None
            output_per_page = int(query_params["per_page"]) if "per_page" in query_params else None

        return ListuserSegmentsResponse(
            user_segments=user_segment,
            per_page=output_per_page,
            page=output_page,
        )
    except HTTPError as e:
        error_response = e.response.json()
        error_message = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return ListuserSegmentsResponse(
            user_segments=[],
            page=None,
            per_page=None,
            http_code=e.response.status_code,
            error_message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return ListuserSegmentsResponse(
            user_segments=[],
            page=None,
            per_page=None,
            http_code=500,
            error_message=str(e),
        )
