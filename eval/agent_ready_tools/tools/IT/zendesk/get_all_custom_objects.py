from http import HTTPStatus
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class CustomObject:
    """Represents a single custom object."""

    custom_object_key: str


@dataclass
class GetAllCustomObjectsResponse:
    """Represents the result of retrieving all custom objects from Zendesk."""

    custom_objects: List[CustomObject]
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def get_all_custom_objects() -> GetAllCustomObjectsResponse:
    """
    Gets the available custom objects configured in Zendesk.

    Returns:
        The list of available custom objects.
    """
    try:
        client = get_zendesk_client()
        response = client.get_request(entity="custom_objects")

        custom_objects: List[CustomObject] = [
            CustomObject(custom_object_key=item.get("key", ""))
            for item in response.get("custom_objects", [])
        ]

        return GetAllCustomObjectsResponse(custom_objects=custom_objects)

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        error_message = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return GetAllCustomObjectsResponse(
            custom_objects=[],
            error_message=error_message,
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
        )
    except Exception as e:  # pylint: disable=broad-except
        return GetAllCustomObjectsResponse(
            custom_objects=[],
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_message=str(e),
        )
