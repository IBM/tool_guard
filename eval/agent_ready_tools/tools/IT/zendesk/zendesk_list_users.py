from http import HTTPStatus
from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class UserInfo:
    """Represents details of a user in Zendesk."""

    user_id: str
    name: str
    email: str
    alias: Optional[str] = None
    role: Optional[str] = None
    active: Optional[bool] = None
    phone: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


@dataclass
class ZendeskUserListResponse:
    """Represents the result of a user list and a message in Zendesk."""

    users: List[UserInfo]
    page: Optional[int] = None
    per_page: Optional[int] = None
    http_code: Optional[int] = None
    message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def zendesk_list_users(
    name: Optional[str] = None,
    email: Optional[str] = None,
    per_page: Optional[int] = 10,
    page: Optional[int] = 1,
) -> ZendeskUserListResponse:
    """
    Retrieves Zendesk user records, optionally filtered by name or email.

    Args:
        name: Filter users by name in Zendesk.
        email: Filter users by email in Zendesk.
        per_page: Number of users to retrieve per page. Defaults to 10.
        page: Page number to retrieve. Defaults to 1.

    Returns:
        A ZendeskUserListResponse containing a list of UserInfo objects and pagination details.
    """
    try:
        client = get_zendesk_client()
        params: Dict[str, Any] = {"per_page": per_page, "page": page}

        if name or email:
            # Use search endpoint for filtering
            query_parts = ["type:user"]
            if name:
                query_parts.append(f'name:"{name}"')
            if email:
                query_parts.append(f'email:"{email}"')

            params["query"] = " ".join(query_parts)
            response = client.get_request(entity="search", params=params)
            users_data = response.get("results", [])
        else:
            # Use users endpoint for listing all
            response = client.get_request(entity="users", params=params)
            users_data = response.get("users", [])

        if not users_data:
            return ZendeskUserListResponse(users=[], message="No data or no match found.")

        result = [
            UserInfo(
                user_id=str(user.get("id")),
                name=user.get("name") or "",
                email=user.get("email") or "",
                alias=user.get("alias"),
                role=user.get("role"),
                active=user.get("active"),
                phone=user.get("phone"),
                notes=user.get("notes"),
                custom_fields=user.get("user_fields"),
            )
            for user in users_data
            if user.get("id")
        ]

        output_page = None
        output_per_page = None
        next_api_link = response.get("next_page")
        if next_api_link:
            query_params = get_query_param_from_links(next_api_link)
            output_page = int(query_params["page"]) if "page" in query_params else None
            output_per_page = int(query_params["per_page"]) if "per_page" in query_params else None

        return ZendeskUserListResponse(users=result, page=output_page, per_page=output_per_page)

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        error_message = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return ZendeskUserListResponse(
            users=[], http_code=e.response.status_code, message=error_message
        )
    except Exception as e:  # pylint: disable=broad-except
        return ZendeskUserListResponse(
            users=[], http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, message=str(e)
        )
