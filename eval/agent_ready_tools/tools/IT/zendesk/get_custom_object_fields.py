from http import HTTPStatus
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class CustomObjectField:
    """Represents a single custom field."""

    field_id: str
    field_type: str
    title: str
    key: Optional[str] = None


@dataclass
class CustomObjectFieldsResponse:
    """Represents the result of retrieving all custom fields from Zendesk."""

    custom_object_fields: List[CustomObjectField]
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def get_custom_object_fields(custom_object_key: str) -> CustomObjectFieldsResponse:
    """
    Gets the configured fields for a custom object in Zendesk.

    Args:
        custom_object_key: The Key of the custom object for updating a record in Zendesk.

    Returns:
        The result from performing the retreiving of custom object fields.
    """
    try:
        client = get_zendesk_client()

        response = client.get_request(entity=f"custom_objects/{custom_object_key}/fields")
        custom_object_fields: List[CustomObjectField] = []

        for result in response["custom_object_fields"]:
            custom_object_fields.append(
                CustomObjectField(
                    field_id=str(result.get("id", "")),
                    field_type=result.get("type", ""),
                    title=result.get("title", ""),
                    key=result.get("key", ""),
                )
            )
        return CustomObjectFieldsResponse(custom_object_fields=custom_object_fields)
    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        if e.response.status_code == HTTPStatus.NOT_FOUND:
            error_message = f"The specified custom object {custom_object_key} does not exist. Please provide valid custom object key and try again."
        else:
            error_message = (
                error_response.get("description", "An unexpected error occurred.")
                if error_response
                else "An unexpected error occurred."
            )
        return CustomObjectFieldsResponse(
            custom_object_fields=[],
            http_code=e.response.status_code,
            error_message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return CustomObjectFieldsResponse(
            custom_object_fields=[],
            http_code=500,
            error_message=str(e),
        )
