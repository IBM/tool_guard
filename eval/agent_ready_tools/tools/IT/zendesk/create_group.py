from http import HTTPStatus
from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class CreateGroupResponse:
    """Represents the result of creating a group in Zendesk."""

    group_name: Optional[str] = None
    id: Optional[str] = None
    is_public: Optional[bool] = None
    description: Optional[str] = None
    error_message: Optional[str] = None
    http_code: Optional[int] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def create_group(
    group_name: str, description: Optional[str] = None, is_public: Optional[bool] = None
) -> CreateGroupResponse:
    """
    Creates a group in Zendesk.

    Args:
        group_name: The name of the group in Zendesk.
        description: The description of the group in Zendesk.
        is_public: It describes whether the group is public or private in Zendesk.

    Returns:
        Details of the created group in Zendesk.
    """
    try:
        client = get_zendesk_client()

        payload: dict[str, Any] = {
            "group": {"name": group_name, "description": description, "is_public": is_public}
        }

        group_payload = payload.get("group") or {}
        payload["group"] = {key: value for key, value in group_payload.items() if value is not None}

        response = client.post_request(entity="groups", payload=payload)
        group_data = response.get("group", {})
        return CreateGroupResponse(
            id=str(group_data.get("id", "")),
            group_name=group_data.get("name", ""),
            description=group_data.get("description", ""),
            is_public=group_data.get("is_public", ""),
        )
    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else {}
        error_message = (
            error_response.get("details", {}).get("name", [])[0].get("description", "")
            if error_response
            else "An unexpected error occurred."
        )
        return CreateGroupResponse(
            error_message=error_message,
            http_code=(
                e.response.status_code
                if e.response.status_code
                else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
        )

    except Exception as e:  # pylint: disable=broad-except
        return CreateGroupResponse(
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_message=str(e),
        )
